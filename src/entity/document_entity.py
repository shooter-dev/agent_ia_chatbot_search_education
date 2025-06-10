# ETAPE 1 / ENTITÉ DOCUMENT /

class Document:
    id: int
    title: str
    content: str
    def __init__(self, id: int, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content
    
    def __repr__(self):
        return f"Document(id={self.id}, title='{self.title}', content='{self.content}')" 
    
# ETAPE 2 / FONCTIONS DE CHARGEMENT DES DOCUMENTS /

import os
import pandas as pd
import xml.etree.ElementTree as ET
from document_entity import Document

DATA_DIR = "data"

def load_documents_from_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)
    documents = []

    for idx, row in df.iterrows():
        content = row.to_string()
        documents.append(Document(id=idx, title=f"CSV-{idx}", content=content))
    
    return documents

def load_documents_from_xml(filename):
    path = os.path.join(DATA_DIR, filename)
    tree = ET.parse(path)
    root = tree.getroot()
    documents = []

    for idx, fiche in enumerate(root.findall(".//fiche")):
        title = fiche.findtext("intitule", default="Sans titre")
        content = ET.tostring(fiche, encoding="unicode", method="xml")
        documents.append(Document(id=idx, title=title, content=content))
    
    return documents

def load_documents_from_xlsx(filename):
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_excel(path)
    documents = []

    for idx, row in df.iterrows():
        content = row.to_string()
        documents.append(Document(id=idx, title=f"XLSX-{idx}", content=content))
    
    return documents

# ETAPE 3 / FONCTION DE VÉRIFICATION DES DOCUMENTS / 

def verify_documents(documents):
    for doc in documents:
        assert isinstance(doc.id, int), f"ID invalide: {doc.id}"
        assert isinstance(doc.title, str) and doc.title.strip(), f"Titre vide: {doc.title}"
        assert isinstance(doc.content, str) and doc.content.strip(), f"Contenu vide: {doc.content}"

        
# ETAPE 4 / FONCTION DE SAUVEGARDE DES DOCUMENTS /

def save_documents(documents, filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(f"{doc.id},{doc.title},{doc.content}\n")

# ETAPE 5 / FONCTION D'AFFICHAGE DES DOCUMENTS /

def main():
    # 1. Chargement des documents
    csv_docs = load_documents_from_csv("fr-en-liste-diplomes-professionnels.csv")
    xml_docs = load_documents_from_xml("Onisep_Ideo_Fiches_Metiers_20052025.xml")
    xlsx_docs = load_documents_from_xlsx("ROME Arborescence Principale 24M06.xlsx")
    
    # 2. Fusion des documents
    all_documents = csv_docs + xml_docs + xlsx_docs
    
    # 3. Vérification
    verify_documents(all_documents)
    
    # 4. Affichage simple
    print(f"\n✅ {len(all_documents)} documents chargés avec succès.\n")
    print("🔎 Aperçu des premiers documents :\n")
