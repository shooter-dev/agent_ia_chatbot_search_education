# Documentation du project

# Assistant Conversationnel IA pour l'Accès à l'Information Publique

## 🎯 Objectif du projet

Dans une démarche de modernisation des services publics, ce projet vise à concevoir un assistant conversationnel intelligent facilitant l'accès à l'information administrative pour les citoyens.

### 🚀 L'assistant permettra : 

🔎 Une recherche contextuelle dans des documents institutionnels (CSV, XML, XLXS).
🧠 Gestion de la mémoire conversationnelle pour des réponses personnalisées.
🛠 Outils avancés : résumé automatique, simplification du langage, calculs d’éligibilité.
💬 Dialogue fluide via une interface web interactive avec restriction contextuelle du domaine.

## ⚙️ Technologies utilisées

- ✅ LangChain → Gestion du RAG (Retrieval-Augmented Generation).
- ✅ ChromaDB → Stockage et recherche vectorielle des documents.
- ✅ Streamlit → Interface web interactive pour l'utilisateur.
- ✅ Python → Développement du backend et des traitements IA.
- ✅ Git → Versionnement et collaboration. 

## 🏗️ Architecture du projet

### 1️⃣ Chargement & Indexation des Documents

- 📂 Lecture des documents avec LangChain DocumentLoaders.
- 🧩 Préparation des données avec Text Splitter (Tokenisation & Chunks).
- 🔎 Indexation vectorielle avec ChromaDB pour le RAG. 

### 2️⃣ Traitement & Interaction IA

- 🛠 Embeddings des documents avec Deepseek
- 🤖 Agent intelligent utilisant LangChain pour répondre aux questions.
- 🧠 Mémoire conversationnelle pour contextualiser les réponses.

### 3️⃣ Interface Web & UX

- 🎨 Développement de l’interface utilisateur avec Streamlit.
- 💬 Interaction fluide avec suggestions dynamiques et restrictions contextuelles.

## 🔹 Installation & Configuration

### 📌 1️⃣ Prérequis

- 🐍 Python 3.10.10
- 📦 Environnement virtuel (venv ou conda)
- 🚀 OpenAI API Key (ou alternative gratuite)

### 🔧 2️⃣ Installation

Clone le projet :

```
git clone https://github.com/shooter-dev/agent_ia_chatbot_search_education.git
cd agent_ia_chatbot_search_education
```

Installe les dépendances :

```
pip install -r requirements.txt
```

### 🛠️ 3️⃣ Configuration

Ajoute une clé DEEPSEEK dans .env :

```
export DEEPSEEK_API_KEY="clé_api_deepseek"
```

Lance l’application Streamlit :

````
streamlit run app.py
````

## 📚 Ressources

LangChain Documentation

ChromaDB Documentation

Streamlit Guide

# Author
[[Elvis](https://github.com/elvis-messiaen), [Amina](https://github.com/elvis-messiaen)]