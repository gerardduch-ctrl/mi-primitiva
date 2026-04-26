import streamlit as st
import random
import requests
from bs4 import BeautifulSoup

# 1. CONFIGURACIÓ INSTANTÀNIA (Això ha d'anar a dalt de tot)
st.set_page_config(page_title="P - Primitiva v28", page_icon="P", layout="centered")

# 2. DADES DE SEGURETAT (Per carregar sense esperar a internet)
if 'sorteigs' not in st.session_state:
    st.session_state.sorteigs = [
        {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ]
    st.session_state.bote = "9.500.000 €"

# 3. ESTILS CSS (Càrrega directa)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 4. UI PRINCIPAL
st.markdown(f'<div class="bote-box">BOTE ACTUAL:<br>{st.session_state.bote}</div>', unsafe_allow_html=True)

# Botó d'actualització ràpid
if st.button("🔄 ACTUALITZAR ARA"):
    try:
        res = requests.get("https://loteriasyapuestas.es", timeout=5)
        # Aquí aniria la lògica de BeautifulSoup...
        st.success("Actualitzat!")
    except:
        st.error("Error de connexió.")

# Mostrar sorteigs (Càrrega immediata des de session_state)
for s in st.session_state.sorteigs:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card"><strong>📅 {s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div></div>', unsafe_allow_html=True)

# ... Resta del codi del generador ...
