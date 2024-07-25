import logging
import uvicorn
from contextlib import asynccontextmanager
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from logging import Logger
from pathlib import Path
from typing import AsyncGenerator
from .controllers import APP_CONTROLLERS, AppBaseController
from .exceptions.app_base_exception import AppBaseException
from .logging.logging_builder import LoggingBuilder
from .middleware.request_identification_middleware import RequestIdentificationMiddleware
from .persistence.app_persistence_context import AppPersistenceContext
from .services.directory_handler import DirectoryHandler
from .settings.app_settings import AppSettings
from .use_cases.audio_samples_deleter import AudioSamplesDeleter


logging.getLogger('asyncio').propagate = False
logging.getLogger('multipart').propagate = False


class App(FastAPI):

    _log: Logger = logging.getLogger(__name__)
    _app_persistence_context: AppPersistenceContext
    _frontend_build_path: Path
    _host: str
    _port: int
    _audio_samples_deleter: AudioSamplesDeleter

    @inject
    def __init__(
        self,
        app_persistence_context: AppPersistenceContext = Provide['app_persistence_context'],
        directory_handler: DirectoryHandler = Provide['directory_handler'],
        app_settings: AppSettings = Provide['app_settings'],
        audio_samples_deleter: AudioSamplesDeleter = Provide['audio_samples_deleter']
    ) -> None:

        super().__init__(
            docs_url='/api/docs',
            openapi_url='/api/openapi.json',
            title=app_settings.app_name,
            lifespan=self._handle_lifespan_events
        )
        self.add_exception_handler(exc_class_or_status_code=Exception, handler=self._handle_exception)
        self.add_middleware(RequestIdentificationMiddleware)
        self._add_controllers()
        self._app_persistence_context = app_persistence_context
        self._frontend_build_path = directory_handler.create_directory(app_settings.server_settings.frontend_build_path)
        self._host = app_settings.server_settings.host
        self._port = app_settings.server_settings.port
        self._audio_samples_deleter = audio_samples_deleter

    def start(self) -> None:

        self._log.info('Starting application...')

        try:

            self.mount(path='/', app=StaticFiles(directory=self._frontend_build_path, html=True), name='frontend')
            uvicorn.run(app=self, host=self._host, port=self._port, log_config=LoggingBuilder.get_configuration())

        except Exception as exception:

            self._log.error(msg='Stopped application because of exception', extra={'exception': exception})

        finally:

            self._log.info('Application stopped')

    def _add_controllers(self) -> None:

        AppController: type[AppBaseController]
        for AppController in APP_CONTROLLERS:

            app_controller: AppBaseController = AppController()
            self.include_router(app_controller.api_router)

    @staticmethod
    async def _handle_exception(request: Request, exc: Exception) -> JSONResponse:

        if isinstance(exc, AppBaseException):

            return JSONResponse(status_code=exc.status_code, content=str(exc), headers=exc.headers)

        else:

            return JSONResponse(status_code=500, content=f'{exc.__class__.__name__}: {exc}')

    @asynccontextmanager
    async def _handle_lifespan_events(self, app: FastAPI) -> AsyncGenerator[None, None]:

        await self._app_persistence_context.begin()
        await self._audio_samples_deleter.delete()
        yield
        await self._app_persistence_context.dispose()
