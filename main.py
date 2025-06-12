from src.services.agents.agent import Agent, executer_agent
from src.services.llm_rag.llm_rag import LlmRag
from langchain_ollama import OllamaEmbeddings

def main():
    llm_rag = LlmRag(OllamaEmbeddings(model="paraphrase-multilingual"))
    agent = Agent(llm_rag)

    executer_agent(agent)

    messages = agent.memory.messages
    interet = messages[-4].content if len(messages) >= 4 else ""
    competences = messages[-3].content if len(messages) >= 3 else ""
    type_travail = messages[-2].content if len(messages) >= 2 else ""
    description_personnelle = messages[-1].content if len(messages) >= 1 else ""

    response = agent.proposer_metier(interet, competences, type_travail, description_personnelle)
    print("Métier suggéré :", response)

if __name__ == "__main__":
    main()
