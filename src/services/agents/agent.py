from src.services.agents.agent_interface import IAgent
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import hub

class Agent(IAgent):
    def __init__(self):
        super().__init__()
        load_dotenv(override=True)
        self.model = ChatOllama(model="llama3", temperature=0)
        self.memory = ConversationBufferMemory()

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
        response = self.model.predict(question)
        historique = self.memory.load_memory_variables({})
        reponses = historique.get(question_type, "").split(", ") if historique.get(question_type) else []
        reponses.append(response)
        self.memory.save_context({question_type: ", ".join(reponses)}, {})
        return response

    def determiner_question_suivante(self):
        historique = self.memory.load_memory_variables({})

        interet = historique.get("interet", "").split(", ") if historique.get("interet") else []
        competences = historique.get("competences", "").split(", ") if historique.get("competences") else []
        type_travail = historique.get("type_travail", "").split(", ") if historique.get("type_travail") else []

        while not interet:
            interet_input = input("Quels sont tes centres d'intérêt ? ")
            if interet_input.strip():
                interet.append(interet_input)
                self.memory.save_context({"interet": ", ".join(interet)}, {})

        while not competences:
            competences_input = input("Quelles sont tes compétences ? ")
            if competences_input.strip():
                competences.append(competences_input)
                self.memory.save_context({"competences": ", ".join(competences)}, {})

        while not type_travail:
            type_travail_input = input("Préféres-tu un travail manuel ou intellectuel ? ")
            if type_travail_input.strip():
                type_travail.append(type_travail_input)
                self.memory.save_context({"type_travail": ", ".join(type_travail)}, {})

        return self.proposer_metier(", ".join(interet), ", ".join(competences), ", ".join(type_travail))

    def proposer_metier(self, interets: str, competences: str, type_travail: str):
        prompt = f"""
        Analyse les informations suivantes et propose un métier adapté :
        - Centres d'intérêt : {interets}
        - Compétences : {competences}
        - Type de travail préféré : {type_travail}

        Utilise ces trois critères pour déterminer un métier qui correspond le mieux à la personne.
        Donne une réponse concise sous la forme : "Un métier adapté pourrait être : [nom du métier]".
        """

        response = self.model.predict(prompt)
        return response

def interet_etudiant(interets: str):
    return f"Tu es intéressé par {interets}. Cela pourrait correspondre à certains métiers."

def competences_etudiant(competences: str):
    return f"Tu as des compétences en {competences}. Cela peut orienter vers des métiers spécifiques."

def type_travail(choix: str):
    return f"Tu préfères un travail {choix}. Cela réduit les options de métiers."

agent = Agent()

tools = [
    Tool(name="interet", func=interet_etudiant, description="Définir les centres d'intérêt."),
    Tool(name="competences", func=competences_etudiant, description="Définir les compétences."),
    Tool(name="type_travail", func=type_travail, description="Définir si le métier est manuel ou intellectuel."),
    Tool(name="proposer_metier", func=agent.proposer_metier, description="Proposer un métier en fonction des réponses.")
]

def executer_agent(agent):
    agent.determiner_question_suivante()

    historique = agent.memory.load_memory_variables({})
    interet = ", ".join(historique.get("interet", "").split(", "))
    competences = ", ".join(historique.get("competences", "").split(", "))
    type_travail = ", ".join(historique.get("type_travail", "").split(", "))

    response = agent.proposer_metier(interet, competences, type_travail)
    return {"response": response}
