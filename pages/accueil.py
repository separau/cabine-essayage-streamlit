import streamlit as st

st.set_page_config(page_title="Accueil", layout="wide")

# Titre principal avec icône
st.markdown("<h1 style='font-size: 3em;'>👗 Bienvenue dans la cabine d’essayage virtuelle</h1>", unsafe_allow_html=True)

# Alerte sur la dépréciation (optionnel)
st.info("ℹ️ Le paramètre `use_column_width` a été supprimé. Veuillez utiliser `use_container_width` à la place.")

# Image de bienvenue
st.image("images/home.png", use_column_width=True)

# Description de l'application
st.write("""
Cette application vous permet d’essayer virtuellement des vêtements grâce à votre **webcam** ou en **uploadant une photo** 🖼️  
👉 Utilisez le menu à gauche pour accéder à l’essayage.
""")
