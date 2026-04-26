import streamlit as st
import random
import requests
from bs4 import BeautifulSoup

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Pro v28", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .update-btn>button { background-color: #f0f2f6 !important; color: black !important; border: 1px solid black !important; height: 40px !important; }
    .gen-btn>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓ DE CONNEXIÓ (ACTUALITZACIÓ) ---
def actualitzar_dades_online():
    try:
        url = "https://loteriasyapuestas.es"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        sorteigs = []
        items = soup.select('.c-cuerpo-reparto-premios')
        for item in items[:3]:
            data = item.select_one('.c-cuerpo-reparto-premios__fecha').get_text(strip=True)
            bolas = [int(n.get_text(strip=True)) for n in item.select('.c-cuerpo-reparto-premios__combinacion-numero')][:6]
            reintegro = item.select_one('.c-cuerpo-reparto-premios__combinacion-reintegro').get_text(strip=True)
            sorteigs.append({"data": data, "nums": sorted(bolas), "r": reintegro})
            
        bote = soup.select_one('.c-anuncio-proximo-sorteo__importe').get_text(strip=True)
        return sorteigs, bote
    except:
        return None, None

# --- DADES INICIALS (Per defecte) ---
if 'sorteigs' not in st.session_state:
    st.session_state.sorteigs = [
        {"data": "Sábado 25 de abril de 2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Jueves 23 de abril de 2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Lunes 20 de abril de 2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ]
    st.session_state.bote = "9.500.000 €"

# --- UI: BOTE I BOTÓ ACTUALITZAR ---
st.markdown(f'<div class="bote-box">BOTE ACTUAL:<br>{st.session_state.bote}</div>', unsafe_allow_html=True)

st.markdown('<div class="update-btn">', unsafe_allow_html=True)
if st.button("🔄 ACTUALITZAR HISTÒRIC (Connexió online)"):
    with st.spinner("Connectant amb Loterías y Apuestas..."):
        n_sorteigs, n_bote = actualitzar_dades_online()
        if n_sorteigs:
            st.session_state.sorteigs = n_sorteigs
            st.session_state.bote = n_bote
            st.success("Dades actualitzades correctament!")
        else:
            st.error("No s'ha pogut connectar. Es mantenen les dades en memòria.")
st.markdown('</div>', unsafe_allow_html=True)

# --- ANÀLISI HISTÒRIC AMB DIAGNÒSTIC ---
st.subheader("Anàlisi Històric")
for s in st.session_state.sorteigs:
    # (Aquí va la teva funció de diagnòstic analitzar_total que ja teníem)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card"><strong>📅 {s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div></div>', unsafe_allow_html=True)

st.divider()

# --- PANELL CONTROL I GENERADOR (Respectant Reintegres 3+3 i Consecutius 1-3-5) ---
# ... (Resta del codi de la v27 amb la lògica de generació de 7 números) ...

st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
if st.button("GENERAR APOSTES MÚLTIPLES (7 NÚM)"):
    # (Lògica de generació v27)
    pass
st.markdown('</div>', unsafe_allow_html=True)
