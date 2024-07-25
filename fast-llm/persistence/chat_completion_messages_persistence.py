import logging
from logging import Logger
from uuid import UUID
from ..domain.chat_completion_message import ChatCompletionMessage


class ChatCompletionMessagesPersistence:

    _log: Logger = logging.getLogger(__name__)
    _chat_history: dict[UUID, list[ChatCompletionMessage]] = {}
    _chat_id: UUID

    def __init__(self, chat_id: UUID) -> None:

        self._chat_id = chat_id

    def get_chat_completion_messages(self) -> list[ChatCompletionMessage]:

        self._log.debug(f'Getting chat completion messages for chat \'{self._chat_id}\'...')
        result: list[ChatCompletionMessage] = self._chat_history.get(self._chat_id, [])
        self._log.debug(f'Chat completion messages for chat \'{self._chat_id}\' found')

        return result

    def save_chat_completion_messages(self, messages: list[ChatCompletionMessage]) -> None:

        self._log.debug(f'Saving chat completion messages for chat \'{self._chat_id}\'...')

        if self._chat_id in self._chat_history:

            self._chat_history[self._chat_id].extend(messages)

        else:

            self._chat_history[self._chat_id] = messages

        self._log.debug(f'Chat completion messages for chat \'{self._chat_id}\' saved')
