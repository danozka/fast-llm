from abc import ABC, abstractmethod
from typing import AsyncGenerator
from ..domain.chat_completion_message import ChatCompletionMessage


class ILargeLanguageModelService(ABC):

    @abstractmethod
    async def get_chat_completion(self, messages: list[ChatCompletionMessage]) -> ChatCompletionMessage:

        raise NotImplementedError

    @abstractmethod
    async def stream_chat_completion(
        self,
        messages: list[ChatCompletionMessage]
    ) -> AsyncGenerator[ChatCompletionMessage, None]:

        raise NotImplementedError
