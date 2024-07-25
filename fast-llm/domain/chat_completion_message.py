from dataclasses import dataclass
from .chat_completion_role_type import ChatCompletionRoleType


@dataclass
class ChatCompletionMessage:

    role: ChatCompletionRoleType
    content: str
