from src.services.agents.agent_interface import IAgent
import os
from IPython.display import display, clear_output, Markdown
from dotenv import load_dotenv
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_deepseek import ChatDeepSeek
from langchain import hub
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory

class Agent(IAgent):

    load_dotenv(override=True)

    model = ChatOllama(model="llama3", temperature=0)
