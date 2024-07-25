import logging
from logging import Logger
from typing import AsyncGenerator
from uuid import UUID
from ..domain.chat_completion_request import ChatCompletionRequest


class ChatCompletionStreamingGetter:

    _log: Logger = logging.getLogger(__name__)
    _chat_id: UUID

    def __init__(self, chat_id: UUID) -> None:

        self._chat_id = chat_id

    async def get(self, message: str) -> AsyncGenerator[str, None]:

        self._log.debug(f'Starting chat completion streaming for message [{message}]...')
        yield ''
        self._log.debug(f'Ending chat completion streaming for message [{message}]...')
