from src.services.agents.agent_interface import IAgent
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor

class Agent(IAgent):
    def __init__(self):
        super().__init__()
        load_dotenv(override=True)
        self.model = ChatOllama(model="llama3", temperature=0)

def interet_etudiant(interets: str):
    return f"Tu es intéressé par {interets}. Cela pourrait correspondre à certains métiers."

def competences_etudiant(competences: str):
    return f"Tu as des compétences en {competences}. Cela peut orienter vers des métiers spécifiques."

def type_travail(choix: str):
    return f"Tu préfères un travail {choix}. Cela réduit les options de métiers."

def proposer_metier(interets: str, competences: str, type_travail: str):
    return f"En fonction de tes intérêts ({interets}), compétences ({competences}) et préférence ({type_travail}), un métier adapté pourrait être 'Ingénieur logiciel' ou 'Artisan menuisier'."

tools = [
    Tool(name="interet", func=interet_etudiant, description="Définir les centres d'intérêt."),
    Tool(name="competences", func=competences_etudiant, description="Définir les compétences."),
    Tool(name="type_travail", func=type_travail, description="Définir si le métier est manuel ou intellectuel."),
    Tool(name="proposer_metier", func=proposer_metier, description="Proposer un métier en fonction des réponses.")
]
