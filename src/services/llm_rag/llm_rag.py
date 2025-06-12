import os
from pathlib import Path
from typing import List

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from src.services.llm_rag.llm_rag_interface import ILlmRag


class LlmRag(ILlmRag):

    def __init__(self, embedder):
        self.embedder = embedder

        db = Chroma(persist_directory=os.path.join(Path(__file__).parents[3], "data", "db"), embedding_function=self.embedder)

        # Conversion de la base Chroma en "retriever" pour effectuer des recherches par similarité
        # - search_type="similarity" utilise la distance cosinus entre les vecteurs
        # - "k": 3 signifie que l'on souhaite récupérer les 3 documents les plus proches

        self.retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )

    def generate_responce(self, question: str) -> str:
        pass

    def search_contex(self, question: str) -> str:
        relevant_chunks = self.retriever.invoke(question)

        return [chunk.page_content for chunk in relevant_chunks]

if __name__ == "__main__":

    llm = LlmRag(OllamaEmbeddings(model="paraphrase-multilingual"))

    rep = llm.search_contex("Quels sont les metier qui utilise l'électronique")

    print(rep)