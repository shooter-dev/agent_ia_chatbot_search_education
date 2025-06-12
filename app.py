import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Découverte de métier",
    page_icon=":mag_right:",
    layout="wide",
    initial_sidebar_state="expanded"
)

sys.path.insert(0, os.path.abspath("src"))

from src.services.agents.agent import Agent
from src.services.llm_rag.llm_rag import LlmRag
from langchain_ollama import OllamaEmbeddings

if 'agent' not in st.session_state:
    try:
        embeddings = OllamaEmbeddings(model="paraphrase-multilingual")
        llm_rag = LlmRag(embeddings)
        st.session_state.agent = Agent(llm_rag)
    except Exception as e:
        st.error("Erreur de connexion à Ollama. Veuillez vérifier que le service est en cours d'exécution.")
        st.stop()


def load_css(file_name):
    try:
        # Vérifier si le fichier existe
        if not os.path.exists(file_name):
            st.error(f"Le fichier CSS n'existe pas : {file_name}")
            return ""
            
        # Lire le contenu du fichier
        with open(file_name, "r", encoding="utf-8") as f:
            css = f.read()
            if not css:
                st.error("Le fichier CSS est vide")
                return ""
            return css
    except Exception as e:
        st.error(f"Erreur lors du chargement du CSS : {str(e)}")
        return ""

# Charger et appliquer le CSS
css = load_css("app.css")
if css:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


st.markdown('<h1 class="custom-title">Découverte de métier avec IA</h1>', unsafe_allow_html=True)
st.markdown("""<p class="text_presentation">
    Découvrez le métier fait pour vous grâce à l'IA !<br>
    Vous vous demandez quel métier correspond le mieux à votre personnalité, vos compétences et vos aspirations ? 
    Notre application, alimentée par l'intelligence artificielle, est là pour vous guider !<br>
    En répondant à une série de questions adaptées à votre profil, notre IA analyse vos réponses 
    et vous propose des métiers qui correspondent à vos centres d'intérêt et à vos aptitudes.
</p>""", unsafe_allow_html=True)

if 'responses' not in st.session_state:
    st.session_state.responses = {}

if 'current_question' not in st.session_state:
    st.session_state.current_question = 1
    st.session_state.questions = st.session_state.agent.determiner_question_suivante()

if st.session_state.current_question <= len(st.session_state.questions):
    current_q = st.session_state.questions[st.session_state.current_question - 1]
    st.markdown(f"### Question {st.session_state.current_question}")
    response = st.text_input(current_q, key=f"question_{st.session_state.current_question}")

    if response:
        st.session_state.responses[st.session_state.current_question] = response
        st.markdown(f'<p class="input-text">Je prends note de ta réponse : {response}</p>',
                    unsafe_allow_html=True)
        st.session_state.current_question += 1
        st.rerun()

if len(st.session_state.responses) == len(st.session_state.questions):
    with st.spinner('Analyse en cours...'):
        try:
            response = st.session_state.agent.proposer_metier(
                st.session_state.responses[1],
                st.session_state.responses[2],
                st.session_state.responses[3],
                st.session_state.responses[4]
            )

            st.markdown(f'<div class="result-text">Le métier qui vous correspond le mieux est : <span class="metier">{response}</span></div>', 
                       unsafe_allow_html=True)

            description = st.session_state.agent.llm_rag.generate_response(
                f"Donne une description détaillée du métier de {response}"
            )
            st.markdown(f'<div class="text_presentation">{description}</div>', 
                       unsafe_allow_html=True)

            explication = st.session_state.agent.llm_rag.generate_response(
                f"Explique pourquoi le métier de {response} correspond aux critères suivants : "
                f"Intérêts : {st.session_state.responses[1]}, "
                f"Compétences : {st.session_state.responses[2]}, "
                f"Type de travail : {st.session_state.responses[3]}, "
                f"Description personnelle : {st.session_state.responses[4]}"
            )
            st.markdown(f'<div class="text_presentation">{explication}</div>', 
                       unsafe_allow_html=True)

        except Exception as e:
            st.error("Une erreur est survenue lors de l'analyse. Veuillez réessayer.")
