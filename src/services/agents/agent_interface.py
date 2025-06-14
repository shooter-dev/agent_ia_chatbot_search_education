import abc
from typing import List
from langchain_core.tools import Tool

class IAgent(abc.ABC):

    @abc.abstractmethod
    def create_react_agent(self, tools: List[Tool]):
        pass

    @abc.abstractmethod
    def executor(self, tools: List[Tool]):
        pass

    @abc.abstractmethod
    def poser_question(self, question: str, question_type: str) -> str:
        pass

    @abc.abstractmethod
    def determiner_question_suivante(self) -> List[str]:
        pass

    @abc.abstractmethod
    def proposer_metier(self, interets: str, competences: str, type_travail: str, description_personnelle: str) -> str:
        pass

