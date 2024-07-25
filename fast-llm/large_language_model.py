from llama_cpp import Llama
from llama_cpp.llama_types import (
    ChatCompletionRequestMessage,
    ChatCompletionRequestSystemMessage,
    ChatCompletionStreamResponseDelta,
    CreateChatCompletionStreamResponse
)
from pathlib import Path
from typing import Generator


class LargeLanguageModel(Llama):

    _system_message: ChatCompletionRequestSystemMessage
    _message_history: list[ChatCompletionRequestMessage]

    def __init__(
        self,
        model_path: Path,
        context_length: int,
        number_of_gpu_layers: int,
        system_message_content: str
    ) -> None:

        super().__init__(
            model_path=str(model_path),
            n_ctx=context_length,
            n_gpu_layers=number_of_gpu_layers,
            verbose=True
        )
        self._system_message = {
            'role': 'system',
            'content': system_message_content
        }
        self._message_history = []

    def stream_chat_completion(self, user_message_content: str) -> Generator[str, None, None]:

        self._message_history.append(
            {
                'role': 'user',
                'content': user_message_content
            }
        )
        input_messages: list[ChatCompletionRequestMessage] = [
            self._system_message,
            *self._message_history
        ]
        assistant_message_content: str = ''

        stream_response: CreateChatCompletionStreamResponse
        for stream_response in self.create_chat_completion(messages=input_messages, stream=True):

            stream_response_delta: ChatCompletionStreamResponseDelta = stream_response['choices'][0]['delta']

            if 'content' in stream_response_delta:

                stream_message_content: str = stream_response_delta['content']
                assistant_message_content += stream_message_content

                yield stream_message_content

        self._message_history.append(
            {
                'role': 'assistant',
                'content': assistant_message_content
            }
        )
