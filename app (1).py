import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
from PIL import Image
import io

# Conexão Atlas
uri = "mongodb+srv://NicoAtividade:rEA4wi11ZbSu5w0L@cluster0.tvdbw2f.mongodb.net/?appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fei"]
faces = db["faces"]

st.title("Reconhecimento Facial - FEI")

# Upload de nova imagem
uploaded_file = st.file_uploader("Envie uma nova foto", type=["jpg","png"])
if uploaded_file:
    img = Image.open(uploaded_file).convert("L")  # cinza
    st.image(img, caption="Imagem enviada", use_column_width=True)

    # Converter para vetor (exemplo simples)
    arr = np.array(img.resize((100,100))).flatten()

    # Comparar com base (exemplo: distância euclidiana)
    best_match = None
    best_score = float("inf")
    for doc in faces.find().limit(100):  # limitar para teste
        db_arr = np.array(doc["vector"])
        score = np.linalg.norm(arr - db_arr)
        if score < best_score:
            best_score = score
            best_match = doc

    if best_match:
        st.write("Face mais parecida encontrada:")
        st.image(Image.open(io.BytesIO(best_match["image_bytes"])))
