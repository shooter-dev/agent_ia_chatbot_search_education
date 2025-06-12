from src.services.agents.agent_interface import IAgent
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain import hub
from src.services.llm_rag.llm_rag import LlmRag
from langchain_ollama import OllamaEmbeddings

class Agent(IAgent):
    def __init__(self, llm_rag):
        super().__init__()
        load_dotenv(override=True)
        self.model = ChatOllama(model="llama3", temperature=0)
        self.memory = ChatMessageHistory()
        self.llm_rag = llm_rag

    def create_react_agent(self, tools):
        prompt = hub.pull("hwchase17/react")
        prompt += "\nUtilise les outils disponibles pour poser des questions et affiner la réponse."

        agent = create_react_agent(
            llm=self.model,
            tools=tools,
            prompt=prompt
        )
        return agent

    def executor(self, tools):
        executor = AgentExecutor.from_agent_and_tools(
            agent=self.create_react_agent(tools),
            tools=tools,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=True
        )
        return executor

    def poser_question(self, question, question_type):
        response = self.llm_rag.generate_response(question)
        self.memory.add_user_message(question)
        self.memory.add_ai_message(response)
        return response

    def determiner_question_suivante(self):
        self.memory.clear()

        interet = input("Quels sont tes centres d'intérêt ? ").strip()
        competences = input("Quelles sont tes compétences ? ").strip()
        type_travail = input("Préféres-tu un travail manuel ou intellectuel ? ").strip()
        description_personnelle = input("Parlez de vous et de ce que vous pensez pertinent pour l'analyse des métiers : ").strip()

        self.memory.add_user_message("Quels sont tes centres d'intérêt ?")
        self.memory.add_ai_message(interet)

        self.memory.add_user_message("Quelles sont tes compétences ?")
        self.memory.add_ai_message(competences)

        self.memory.add_user_message("Préféres-tu un travail manuel ou intellectuel ?")
        self.memory.add_ai_message(type_travail)

        self.memory.add_user_message("Parlez de vous et de ce que vous pensez pertinent pour l'analyse des métiers :")
        self.memory.add_ai_message(description_personnelle)

        return self.proposer_metier(interet, competences, type_travail, description_personnelle)

    def proposer_metier(self, interets: str, competences: str, type_travail: str, description_personnelle: str):
        recherche_question = f"Quels métiers correspondent aux centres d'intérêt '{interets}', aux compétences '{competences}', et à la description personnelle '{description_personnelle}' ?"
        contexte = self.llm_rag.search_context(recherche_question)
        contexte_str = "\n".join(contexte)

        prompt = f"""
        Voici des informations pertinentes sur les métiers liés aux centres d'intérêt, compétences et description personnelle :
        {contexte_str}

        En utilisant ces informations et les préférences suivantes :
        - Centres d'intérêt : {interets}
        - Compétences : {competences}
        - Type de travail préféré : {type_travail}
        - Description personnelle : {description_personnelle}

        Propose un métier adapté sous la forme : "Un métier adapté pourrait être : [nom du métier]".
        Ne propose pas de métiers qui ne correspondent pas aux critères donnés.
        """

        response = self.llm_rag.generate_response(prompt)
        return response

def executer_agent(agent):
    agent.determiner_question_suivante()

    messages = agent.memory.messages
    interet = messages[-4].content if len(messages) >= 4 else ""
    competences = messages[-3].content if len(messages) >= 3 else ""
    type_travail = messages[-2].content if len(messages) >= 2 else ""
    description_personnelle = messages[-1].content if len(messages) >= 1 else ""

    response = agent.proposer_metier(interet, competences, type_travail, description_personnelle)
    print("Métier suggéré :", response)
