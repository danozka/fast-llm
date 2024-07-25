from enum import Enum


class ChatCompletionRoleType(int, Enum):

    assistant = 0
    system = 1
    user = 2
