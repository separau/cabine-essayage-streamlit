
import streamlit as st
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="Cabine d’essayage virtuelle", page_icon="👗", layout="wide")

# Titre principal
st.markdown("<h1 style='text-align: center;'>👗 Bienvenue dans la cabine d’essayage virtuelle</h1>", unsafe_allow_html=True)

# Charger l'image d'accueil
try:
    image_path = "images/home.png"  # Assurez-vous que ce fichier est bien présent
    image = Image.open(image_path)
    st.image(image, caption="", use_container_width=True)
except FileNotFoundError:
    st.warning("L'image d'accueil 'home.png' est introuvable. Veuillez la placer dans le dossier 'images'.")

# Description
st.markdown("""
<div style='text-align: center; font-size:18px;'>
Cette application vous permet d’essayer virtuellement des vêtements grâce à votre <b>webcam</b> ou en <b>uploadant une photo</b> 📸<br><br>
👉 Utilisez le menu à gauche pour accéder à l’essayage.
</div>
""", unsafe_allow_html=True)
