import os
from pathlib import Path

from langchain_community.document_loaders import CSVLoader, UnstructuredXMLLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 📂 Répertoire des données
DATA_DIR = f"{Path(__file__).parents[3]}/data"

# 1️⃣ Chargement des documents avec Langchain
def load_documents():
    csv_loader = CSVLoader(file_path=os.path.join(DATA_DIR, "fr-en-liste-diplomes-professionnels.csv"), csv_args={'delimiter': ';'})
    xml_loader = UnstructuredXMLLoader(file_path=os.path.join(DATA_DIR, "Onisep_Ideo_Fiches_Metiers_20052025.xml"))
    xlsx_loader = UnstructuredExcelLoader(file_path=os.path.join(DATA_DIR, "ROME Arborescence Principale 24M06.xlsx"))

    csv_docs = csv_loader.load()
    xml_docs = xml_loader.load()
    xlsx_docs = xlsx_loader.load()

    all_documents = csv_docs + xml_docs + xlsx_docs
    return all_documents

# 2️⃣ Préparation et tokenisation des documents
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    return splitter.split_documents(documents)

# 3️⃣ Embeddings des documents
def embed_documents(documents):
    embeddings = OllamaEmbeddings(model="bge-m3")
    Chroma.from_documents(documents, embeddings, persist_directory=f"{Path(__file__).parents[3]}/data/db")

# 4️⃣ Exécution du pipeline
def main():

    try:
        documents = load_documents()
        tokenized_docs = split_documents(documents)
        embed_documents(tokenized_docs)
        print(f"\n✅ {len(tokenized_docs)} documents chargés, tokenisés et indexés pour le RAG !\n")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()

