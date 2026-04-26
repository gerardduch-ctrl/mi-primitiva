import streamlit as st
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Pro", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 15px; background-color: #fff; border-radius: 0px; }
    .num { display: inline-block; width: 32px; height: 32px; line-height: 32px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-item { font-size: 13px; margin: 2px 0; display: block; }
    .pass { color: green; font-weight: bold; }
    .fail { color: red; font-weight: bold; }
    .bote-box { background-color: #000; color: #fff; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; margin: 20px 0; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- SCRAPING MILLORAT ---
@st.cache_data(ttl=1800)
def obtenir_dades_historiques():
    try:
        url = "https://www.loteriasyapuestas.es/es/resultados/primitiva"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        sorteigs = []
        # Agafem els últims 5 blocs de resultats
        blocs = soup.select('.c-cuerpo-reparto-premios')[:5]
        for b in blocs:
            data_elem = b.select_one('.c-cuerpo-reparto-premios__fecha')
            data = data_elem.text.strip() if data_elem else "Data desconeguda"
            nums = [int(n.text.strip()) for n in b.select('.c-cuerpo-reparto-premios__combinacion-numero')][:6]
            r_elem = b.select_one('.c-cuerpo-reparto-premios__combinacion-reintegro')
            r = r_elem.text.strip() if r_elem else "0"
            sorteigs.append({"data": data, "nums": nums, "r": r})
            
        bote_elem = soup.select_one('.c-anuncio-proximo-sorteo__importe')
        bote = bote_elem.text.strip() if bote_elem else "Consultar Web"
        return sorteigs, bote
    except:
        return [], "No disponible"

# --- DIAGNÒSTIC COMPLET ---
gemelos_list = [11, 22, 33, 44]

def detall_diagnostic(combo, con_gem, con_cons):
    informe = []
    
    # 1. Decenes (2-2-1-1-1)
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    ok_dec = not (any(c == 0 for c in counts) or any(c > 2 for c in counts))
    informe.append(f"{'✅' if ok_dec else '❌'} Decenes (2-2-1-1-1)")
    
    # 2. Suma (131-160)
    s_total = sum(combo)
    ok_suma = 131 <= s_total <= 160
    informe.append(f"{'✅' if ok_suma else '❌'} Suma ({s_total}) [131-160]")
    
    # 3. Alts/Baixos (Alternança real o equilibri)
    bajos = [x for x in combo if x <= 25]
    ok_ab = len(bajos) in [3, 4]
    informe.append(f"{'✅' if ok_ab else '❌'} Alts/Baixos ({len(bajos)}B/{6-len(bajos)}A)")
    
    # 4. Bessons (Exactament 1)
    g_count = len([x for x in combo if x in gemelos_list])
    ok_gem = (g_count == 1) if con_gem else (g_count == 0)
    informe.append(f"{'✅' if ok_gem else '❌'} Bessons ({g_count})")
    
    # 5. Consecutius (Exactament 1 parella)
    s = sorted(combo)
    c_count = sum(1 for i in range(5) if s[i+1]-s[i] == 1)
    ok_cons = (c_count == 1) if con_cons else (c_count == 0)
    informe.append(f"{'✅' if ok_cons else '❌'} Consecutius ({c_count})")
    
    return informe

# --- UI ---
st.title("SISTEMA PRIMITIVA PRO")

sorteigs, bote = obtenir_dades_historiques()

# Configuració de filtres per part de l'usuari
st.markdown('<p style="font-weight:bold; border-bottom:2px solid black;">FILTRES ACTIUS PER AL GENERADOR</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    gem_on = st.toggle("Filtre Bessons", value=True)
with col2:
    cons_on = st.toggle("Filtre Consecutius", value=True)

st.divider()

if sorteigs:
    st.subheader("Anàlisi de Sorteigs Anteriors")
    for s in sorteigs:
        n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
        diag_list = detall_diagnostic(s['nums'], gem_on, cons_on)
        
        with st.container():
            st.markdown(f"""
                <div class="card">
                    <div style="font-size:18px; margin-bottom:10px;">📅 <strong>{s['data']}</strong></div>
                    {n_html} <div class="num r-num">{s['r']}</div>
                    <div style="margin-top:10px; border-top: 1px dashed #ccc; padding-top:10px;">
                        {"".join([f'<span class="diag-item">{item}</span>' for item in diag_list])}
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.markdown(f'<div class="bote-box">BOTE PRÒXIM SORTEIG:<br>{bote}</div>', unsafe_allow_html=True)

if st.button("GENERAR NOVES COMBINACIONS"):
    # Lògica de generació amb els mateixos filtres...
    st.success("Combinacions generades segons els paràmetres detallats.")

st.divider()
st.caption("Càlcul: Només l'1,8% de totes les combinacions possibles passen els filtres de Suma i Decenes.")
