import os
from pathlib import Path
from typing import List

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from src.services.llm_rag.llm_rag_interface import ILlmRag


class LlmRag(ILlmRag):

    def __init__(self, embedder):
        self.embedder = embedder
        self.llm = ChatOllama(model="llama3", temperature=0)

        db_path = os.path.join(Path(__file__).parents[3], "data", "db")
        db = Chroma(persist_directory=db_path, embedding_function=self.embedder)

        self.retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )

    def search_context(self, question: str) -> List[str]:
        relevant_chunks = self.retriever.invoke(question)
        return [chunk.page_content for chunk in relevant_chunks]

    def generate_response(self, question: str) -> str:
        context = self.search_context(question)
        context_str = "\n".join(context)

        prompt = f"""
        Voici des informations pertinentes extraites de la base de données :
        {context_str}

        Réponds uniquement en fonction des informations fournies et des préférences de l'utilisateur.
        Ne propose pas de métiers qui ne correspondent pas aux centres d'intérêt et compétences donnés.

        Question : {question}
        """

        response = self.llm.invoke(prompt)
        return response.content