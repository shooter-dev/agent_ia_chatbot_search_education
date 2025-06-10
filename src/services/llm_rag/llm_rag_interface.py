import abc

class ILlmRag(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_responce(question: str) -> str:
        return ''

    @abc.abstractmethod
    def search_contex(question: str) -> str:
        return ''