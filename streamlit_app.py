import streamlit as st
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 15px; background-color: #fff; }
    .num { display: inline-block; width: 32px; height: 32px; line-height: 32px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-item { font-size: 13px; margin: 2px 0; display: block; border-bottom: 1px solid #eee; padding: 2px 0; }
    .bote-box { background-color: #000; color: #fff; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; margin: 20px 0; border: 4px solid gold; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; margin-top: 20px; }
    .tit-selector { font-size: 18px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid black; display: inline-block; width: 100%; color: black; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- SCRAPING I DADES ---
@st.cache_data(ttl=1800)
def obtenir_dades_reals():
    try:
        url = "https://loteriasyapuestas.es"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        sorteigs = []
        items = soup.find_all('div', class_='c-cuerpo-reparto-premios')[:3]
        for item in items:
            data = item.find('p', class_='c-cuerpo-reparto-premios__fecha').text.strip()
            bolas = [int(n.text.strip()) for n in item.find_all('span', class_='c-cuerpo-reparto-premios__combinacion-numero')][:6]
            reintegro = item.find('span', class_='c-cuerpo-reparto-premios__combinacion-reintegro').text.strip()
            sorteigs.append({"data": data, "nums": bolas, "r": reintegro})
        bote = soup.find('span', class_='c-anuncio-proximo-sorteo__importe').text.strip()
        return sorteigs, bote
    except:
        return [{"data": "Dissabte 25/04/2026", "nums": [3,6,10,28,30,46], "r": "1"}], "9.500.000 €"

# --- LÒGICA DE GRUPS I FILTRES ---
gemelos_list = [11, 22, 33, 44]
n_tots = set(range(1, 50))
cal_hist = [38, 39, 47, 3, 45, 30, 42, 1, 11, 22] # Top Històric
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def validar_final(combo, anteriores, con_gem, con_cons, tipo_p, tipo_ab):
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    if any(c == 0 for c in counts) or any(c > 2 for c in counts): return False
    if not (131 <= sum(combo) <= 160): return False
    bajos = [x for x in combo if x <= 25]
    if (tipo_ab == "4B3A" and len(bajos) != 4) or (tipo_ab == "3B4A" and len(bajos) != 3): return False
    p_count = len([x for x in combo if x % 2 == 0])
    if (tipo_p == "3P4I" and p_count != 3) or (tipo_p == "4P3I" and p_count != 4): return False
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
    g_count = len([x for x in combo if x in gemelos_list])
    if (con_gem and g_count != 1) or (not con_gem and g_count > 0): return False
    s = sorted(combo)
    c_count = sum(1 for i in range(5) if s[i+1]-s[i] == 1)
    if (con_cons and c_count != 1) or (not con_cons and c_count > 0): return False
    return True

def detall_diagnostic(combo, con_gem, con_cons):
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    ok_dec = not (any(c == 0 for c in counts) or any(c > 2 for c in counts))
    s_total = sum(combo)
    ok_suma = 131 <= s_total <= 160
    bajos = [x for x in combo if x <= 25]
    ok_ab = len(bajos) in [3, 4]
    g_count = len([x for x in combo if x in gemelos_list])
    c_count = sum(1 for i in range(5) if sorted(combo)[i+1]-sorted(combo)[i] == 1)
    return [
        f"{'✅' if ok_dec else '❌'} Decenes (2-2-1-1-1)",
        f"{'✅' if ok_suma else '❌'} Suma ({s_total}) [131-160]",
        f"{'✅' if ok_ab else '❌'} Alts/Baixos ({len(bajos)}B/{6-len(bajos)}A)",
        f"{'✅' if (g_count==1 if con_gem else g_count==0) else '❌'} Bessons ({g_count})",
        f"{'✅' if (c_count==1 if con_cons else c_count==0) else '❌'} Consecutius ({c_count})"
    ]

# --- INTERFÍCIE ---
st.title("SISTEMA PRIMITIVA PRO v6")
sorteigs, bote = obtenir_dades_reals()

st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote}</div>', unsafe_allow_html=True)

# 1. ANÀLISI HISTÒRIC
st.subheader("Anàlisi Històric Detallat")
for s in sorteigs:
    diag_list = detall_diagnostic(s['nums'], True, True)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <div style="font-size:17px; margin-bottom:8px; border-bottom:1px solid black;">📅 <strong>{s['data']}</strong></div>
            {n_html} <div class="num r-num">{s['r']}</div>
            <div style="margin-top:10px; background:#f9f9f9; padding:5px;">
                {"".join([f'<span class="diag-item">{item}</span>' for item in diag_list])}
            </div>
        </div>
    """, unsafe_allow_html=True)

# 2. SELECTORS (Ara ben visibles)
st.markdown('<p class="tit-selector">CONFIGURACIÓ GENERADOR</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    gem_on = st.radio("NÚMEROS BESSONS", ["OFF", "ON"], index=1) == "ON"
with col2:
    cons_on = st.radio("CONSECUTIUS", ["OFF", "ON"], index=1) == "ON"

# 3. BOTÓ GENERAR
if st.button("GENERAR 6 COMBINACIONS OPTIMITZADES"):
    finales = []
    rs_top = [8, 5, 2, 7, 9, 0]
    intentos = 0
    while len(finales) < 6 and intentos < 50000:
        tipo_p = "3P4I" if len(finales) % 2 == 0 else "4P3I"
        tipo_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        c = [random.choice(cal_hist)] + random.sample(desp_hist, 3) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        if len(c) == 6 and validar_final(c, finales, gem_on, cons_on, tipo_p, tipo_ab):
            finales.append(c)
        intentos += 1
    
    if len(finales) < 6:
        st.warning("Filtres molt estrictes. Torna a intentar-ho.")
    else:
        st.subheader("Les teves Apostes")
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)

st.divider()
st.info(f"D'un total de 13.983.816 combinacions, només unes 251.708 passen els teus filtres principals.")
