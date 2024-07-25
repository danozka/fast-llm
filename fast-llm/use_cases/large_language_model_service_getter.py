import logging
from logging import Logger
from ..domain.large_language_model_type import LargeLanguageModelType
from ..exceptions.unknown_large_language_model_exception import UnknownLargeLanguageModelException
from ..services.i_large_language_model_service import ILargeLanguageModelService


class LargeLanguageModelServiceGetter:

    _log: Logger = logging.getLogger(__name__)

    def get(self, large_language_model_type: LargeLanguageModelType) -> ILargeLanguageModelService:

        if large_language_model_type == LargeLanguageModelType.llama3:

            self._log.debug('Loading Llama3 model...')
            result: ILargeLanguageModelService = ...
            self._log.debug('Llama3 model loaded successfully')

        else:

            raise UnknownLargeLanguageModelException(large_language_model_type.value)

        return result
