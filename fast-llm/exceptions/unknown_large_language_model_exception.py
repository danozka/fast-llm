class UnknownLargeLanguageModelException(Exception):

    def __init__(self, model_name: str) -> None:

        super().__init__(f'Large Language Model \'{model_name}\' is an unknown value')
