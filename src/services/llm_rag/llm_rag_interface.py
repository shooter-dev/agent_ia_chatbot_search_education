import abc
from typing import List

class ILlmRag(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_response(self, question: str) -> str:
        pass

    @abc.abstractmethod
    def search_context(self, question: str) -> List[str]:
        pass
