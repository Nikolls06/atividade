
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import gridfs
from PIL import Image
import io

# Configuração da conexão
uri = "mongodb+srv://NicoAtividade:rEA4wi11ZbSu5w0L@cluster0.tvdbw2f.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

# Seleciona o banco
db = client["midias"]
fs = gridfs.GridFS(db)

st.title("Visualizador de Arquivos do MongoDB Atlas (GridFS)")

# Lista arquivos disponíveis
files = list(fs.find())
if not files:
    st.warning("Nenhum arquivo encontrado no banco 'midias'.")
else:
    st.write("Arquivos disponíveis:")
    for f in files:
        st.write(f"📂 {f.filename} — {f.length} bytes — {f.upload_date}")

    # Seleciona um arquivo para visualizar
    selected_file = st.selectbox("Escolha um arquivo para visualizar:", [f.filename for f in files])

    if selected_file:
        file = fs.find_one({"filename": selected_file})
        if file:
            try:
                image = Image.open(io.BytesIO(file.read()))
                st.image(image, caption=selected_file)
            except Exception:
                st.error("Esse arquivo não é uma imagem ou não pôde ser exibido.")
