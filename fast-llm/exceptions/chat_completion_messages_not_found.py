from uuid import UUID


class ChatCompletionMessagesNotFound(Exception):

    def __init__(self, chat_id: UUID) -> None:

        super().__init__(f'No chat completion messages found for chat \'{chat_id}\'')
