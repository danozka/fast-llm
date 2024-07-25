from dataclasses import dataclass
from uuid import UUID
from .chat_completion_message import ChatCompletionMessage


@dataclass
class ChatCompletionRequest:

    chat_id: UUID | None
    message: ChatCompletionMessage
