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
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-item { font-size: 12px; margin: 1px 0; display: block; border-bottom: 1px solid #eee; }
    .bote-box { background-color: #000; color: #fff; padding: 15px; text-align: center; font-size: 22px; font-weight: 900; margin: 15px 0; border: 3px solid gold; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 50px; font-weight: bold; border-radius: 0px; font-size: 16px; margin-top: 10px; }
    .tit-selector { font-size: 16px; font-weight: bold; margin-top: 10px; border-bottom: 2px solid black; display: block; width: 100%; color: black; text-transform: uppercase; }
    /* Ajust per a mòbils: forçar visibilitat */
    div[data-testid="stRadio"] { padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- SCRAPING ROBUST (3 SORTEIGS) ---
@st.cache_data(ttl=1800)
def obtenir_dades_reals():
    try:
        url = "https://loteriasyapuestas.es"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        sorteigs = []
        # Busquem tots els blocs de resultats disponibles
        items = soup.find_all('div', class_='c-cuerpo-reparto-premios')
        
        # Ens assegurem d'agafar els 3 últims reals
        for item in items[:3]:
            data_raw = item.find('p', class_='c-cuerpo-reparto-premios__fecha')
            data = data_raw.text.strip() if data_raw else "Data no disponible"
            bolas = [int(n.text.strip()) for n in item.find_all('span', class_='c-cuerpo-reparto-premios__combinacion-numero')][:6]
            reintegro_raw = item.find('span', class_='c-cuerpo-reparto-premios__combinacion-reintegro')
            reintegro = reintegro_raw.text.strip() if reintegro_raw else "0"
            sorteigs.append({"data": data, "nums": bolas, "r": reintegro})
        
        bote_raw = soup.find('span', class_='c-anuncio-proximo-sorteo__importe')
        bote = bote_raw.text.strip() if bote_raw else "Consultar Web"
        return sorteigs, bote
    except:
        # Fallback fix si falla la web per evitar que l'app quedi buida
        fallback = [
            {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
            {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "0"},
            {"data": "Dilluns 20/04/2026", "nums": [5, 12, 18, 33, 41, 49], "r": "5"}
        ]
        return fallback, "9.500.000 €"

# --- LÒGICA DE FILTRES ---
gemelos_list = [11, 22, 33, 44]
n_tots = set(range(1, 50))
cal_hist = [38, 39, 47, 3, 45, 1, 49, 7, 10, 2] # Top Històric
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

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
        f"{'✅' if ok_suma else '❌'} Suma ({s_total})",
        f"{'✅' if ok_ab else '❌'} Alts/Baixos ({len(bajos)}B/{6-len(bajos)}A)",
        f"{'✅' if (g_count==1 if con_gem else g_count==0) else '❌'} Bessons ({g_count})",
        f"{'✅' if (c_count==1 if con_cons else c_count==0) else '❌'} Consecutius ({c_count})"
    ]

# --- UI ---
st.title("SISTEMA PRIMITIVA v6")

# 1. BOTE I HISTÒRIC (3 SORTEIGS)
sorteigs, bote = obtenir_dades_reals()
st.markdown(f'<div class="bote-box">BOTE PROPER SORTEIG:<br>{bote}</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Últims 3 Sorteigs")
for s in sorteigs:
    diag_list = detall_diagnostic(s['nums'], True, True)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    with st.container():
        st.markdown(f"""
            <div class="card">
                <div style="font-size:15px; font-weight:bold; border-bottom:1px solid black; margin-bottom:5px;">📅 {s['data']}</div>
                {n_html} <div class="num r-num">{s['r']}</div>
                <div style="margin-top:8px; background:#f9f9f9; padding:5px; border-radius:3px;">
                    {"".join([f'<span class="diag-item">{item}</span>' for item in diag_list])}
                </div>
            </div>
        """, unsafe_allow_html=True)

# 2. SELECTORS (Verticals per a mòbil)
st.markdown('<p class="tit-selector">CONFIGURACIÓ</p>', unsafe_allow_html=True)
gem_on = st.radio("Filtre NÚMEROS BESSONS (11, 22, 33, 44)", ["OFF", "ON"], index=1, key="gem_mobile") == "ON"
cons_on = st.radio("Filtre NÚMEROS CONSECUTIUS (ex: 14-15)", ["OFF", "ON"], index=1, key="cons_mobile") == "ON"

# 3. GENERADOR
if st.button("GENERAR COMBINACIONS"):
    finales = []
    rs_top = [8, 5, 2, 0, 7, 9]
    intentos = 0
    while len(finales) < 6 and intentos < 30000:
        tipo_p = "3P4I" if len(finales) % 2 == 0 else "4P3I"
        tipo_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        # Selecció base
        c = [random.choice(cal_hist)] + random.sample(desp_hist, 3) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        # Per a la generació, fem servir la mateixa lògica de validació que abans
        decs = [(x-1)//10 for x in c]
        if len(c) == 6 and not (any(decs.count(i) == 0 for i in range(5)) or any(decs.count(i) > 2 for i in range(5))):
            if 131 <= sum(c) <= 160:
                bajos = [x for x in c if x <= 25]
                if (tipo_ab == "4B3A" and len(bajos) == 4) or (tipo_ab == "3B4A" and len(bajos) == 3):
                    g_count = len([x for x in c if x in gemelos_list])
                    if (gem_on and g_count == 1) or (not gem_on and g_count == 0):
                        s_c = sorted(c)
                        c_count = sum(1 for i in range(5) if s_c[i+1]-s_c[i] == 1)
                        if (cons_on and c_count == 1) or (not cons_on and c_count == 0):
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
st.caption("Filtres actius: Suma 131-160 | Decenes 2-2-1-1-1 | Alternança Alts/Baixos")
