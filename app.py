import streamlit as st
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.services.agents.agent import Agent
from src.services.llm_rag.llm_rag import LlmRag
from langchain_ollama import OllamaEmbeddings



def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
    return css


css = load_css("src/streamlint/app.css")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Découverte de métier",
    page_icon=":mag_right:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de l'agent
if 'agent' not in st.session_state:
    embeddings = OllamaEmbeddings(model="paraphrase-multilingual")
    llm_rag = LlmRag(embeddings)
    st.session_state.agent = Agent(llm_rag)

st.markdown('<h1 class="custom-title">Découverte de métier avec IA</h1>', unsafe_allow_html=True)
st.markdown(f"""<p class="text_presentation">Découvrez le métier fait pour vous grâce à l\'IA !
Vous vous demandez quel métier correspond le mieux à votre personnalité, vos compétences et vos aspirations ? Notre application, alimentée par l'intelligence artificielle, est là pour vous guider !
En répondant à une série de questions adaptées à votre profil, notre IA analyse vos réponses et vous propose des métiers qui correspondent à vos centres d'intérêt et à vos aptitudes.
Que vous soyez en pleine réflexion sur votre avenir professionnel ou simplement curieux de découvrir de nouvelles opportunités, cette application vous offre un accompagnement personnalisé.
Grâce à une technologie avancée, nous vous aidons à mieux comprendre vos forces et à explorer des carrières qui vous correspondent vraiment.</p>""",
            unsafe_allow_html=True)

# Initialisation des réponses
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Questions de l'agent
questions = {
    1: "Quels sont tes centres d'intérêt ?",
    2: "Quelles sont tes compétences ?",
    3: "Préféres-tu un travail manuel ou intellectuel ?",
    4: "Parlez de vous et de ce que vous pensez pertinent pour l'analyse des métiers :"
}

# Affichage des questions et collecte des réponses
for step in range(1, 5):
    if step == 1 or st.session_state.responses.get(step - 1):
        st.session_state.responses[step] = st.text_input(questions[step])
        if st.session_state.responses[step]:
            st.markdown(f'<p class="input-text">Je prends note de ta réponse : {st.session_state.responses[step]}.</p>',
                        unsafe_allow_html=True)

# Analyse des réponses quand toutes les questions sont répondues
if all(st.session_state.responses.values()):
    with st.spinner('Analyse en cours...'):
        try:
            # Utilisation de l'agent pour analyser les réponses
            response = st.session_state.agent.proposer_metier(
                st.session_state.responses[1],  # intérêts
                st.session_state.responses[2],  # compétences
                st.session_state.responses[3],  # type de travail
                st.session_state.responses[4]  # description personnelle
            )

            # Affichage du résultat
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.markdown(f'<h3 class="result-text">{response}</h3>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'analyse : {str(e)}")