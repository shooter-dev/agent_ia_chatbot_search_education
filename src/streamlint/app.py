import streamlit as st
import main

def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
    return css

css = load_css("app.css")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Découverte de métier",
    page_icon=":mag_right:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f'<h1 class="custom-title">{main.title}</h1>', unsafe_allow_html=True)
st.markdown(f"""<p class="text_presentation">Découvrez le métier fait pour vous grâce à l\'IA !
Vous vous demandez quel métier correspond le mieux à votre personnalité, vos compétences et vos aspirations ? Notre application, alimentée par l'intelligence artificielle, est là pour vous guider !
En répondant à une série de questions adaptées à votre profil, notre IA analyse vos réponses et vous propose des métiers qui correspondent à vos centres d'intérêt et à vos aptitudes.
Que vous soyez en pleine réflexion sur votre avenir professionnel ou simplement curieux de découvrir de nouvelles opportunités, cette application vous offre un accompagnement personnalisé.
Grâce à une technologie avancée, nous vous aidons à mieux comprendre vos forces et à explorer des carrières qui vous correspondent vraiment.</p>""", unsafe_allow_html=True)

responses = {}

questions = {
    1: main.question1,
    2: main.question2,
    3: main.question3
}

for step in range(1, 4):
    if step == 1 or responses.get(step - 1):
        responses[step] = st.text_input(questions[step])
        if responses[step]:
            st.markdown(f'<p class="input-text">Je prends note de ta réponse : {responses[step]}.</p>', unsafe_allow_html=True)

if all(responses.values()):
    st.markdown('<h3 class="result-text">Le métier qui vous correspond est : <p classe="metier">Développeur</p></h3>', unsafe_allow_html=True)