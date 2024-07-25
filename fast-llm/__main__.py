from pathlib import Path
from .large_language_model import LargeLanguageModel


class Main:

    _llm: LargeLanguageModel

    def __init__(self) -> None:

        print('- AI: Loading Marta\'s present...')
        self._llm = LargeLanguageModel(
            model_path=Path(__file__).parent.resolve().joinpath('model.gguf'),
            context_length=8192,
            number_of_gpu_layers=33,
            system_message_content=(
                'You are an AI assistant that will be talking to Marta. Today is Marta\'s birthday. Marta\'s boyfriend '
                'Daniel has prepared for her a weekend trip to Granada (Spain) as a present. Marta has to guess the '
                'location of the weekend trip. As an AI assistant, you will be giving Marta riddles and clues to help '
                'her guess where she is going to travel. You cannot mention explicitly "Granada" or any other name '
                'that Granada is known for. Also, you cannot mention explicitly the name of any monument or place '
                'inside Granada. She has to guess everything. If she guesses something right, you will tell her so. '
                'The final answer is "Granada".'
            )
        )

    def run(self) -> None:

        self._stream_llm_response(
            'Say hello to Marta, congratulate her on her birthday and explain to her what she has to do'
        )

        while True:

            self._stream_llm_response(self._get_user_input())

    @staticmethod
    def _get_user_input() -> str:

        print('\n-', 'Marta', end=': ')

        return input()

    def _stream_llm_response(self, message: str) -> None:

        print('-', 'AI', end=': ')

        message_chunk: str
        for message_chunk in self._llm.stream_chat_completion(message):

            print(message_chunk, end='')

        print()


main: Main = Main()
main.run()
