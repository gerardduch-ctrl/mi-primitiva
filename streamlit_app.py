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
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; }
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
        items = soup.select('.c-cuerpo-reparto-premios')
        for item in items[:3]:
            data = item.select_one('.c-cuerpo-reparto-premios__fecha').get_text(strip=True)
            bolas = [int(n.get_text(strip=True)) for n in item.select('.c-cuerpo-reparto-premios__combinacion-numero')][:6]
            reintegro = item.select_one('.c-cuerpo-reparto-premios__combinacion-reintegro').get_text(strip=True)
            sorteigs.append({"data": data, "nums": sorted(bolas), "r": reintegro})
        bote = soup.select_one('.c-anuncio-proximo-sorteo__importe').get_text(strip=True)
        return sorteigs, bote
    except:
        # FALLBACK REAL ABRIL 2026
        fallback = [
            {"data": "Sábado 25 de abril de 2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
            {"data": "Jueves 23 de abril de 2026", "nums": [11, 13, 20, 26, 27, 34], "r": "0"},
            {"data": "Lunes 20 de abril de 2026", "nums": [4, 7, 29, 39, 41, 48], "r": "5"}
        ]
        return fallback, "9.000.000 €"

# --- LÒGICA DE FILTRES ---
gemelos_list = [11, 22, 33, 44]
cal_hist = [38, 39, 47, 3, 45, 30, 4, 1, 11, 22]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def detall_diagnostic(combo, con_gem, con_cons):
    decs = [(x-1)//10 for x in combo]
    ok_dec = all(decs.count(i) <= 2 for i in range(5))
    s_total = sum(combo)
    ok_suma = 131 <= s_total <= 160
    bajos = [x for x in combo if x <= 25]
    ok_ab = len(bajos) in [3, 4]
    g_count = len([x for x in combo if x in gemelos_list])
    c_count = sum(1 for i in range(5) if sorted(combo)[i+1]-sorted(combo)[i] == 1)
    return [
        f"{'✅' if ok_dec else '❌'} Decenes (Máx 2 x fila)",
        f"{'✅' if ok_suma else '❌'} Suma ({s_total}) [131-160]",
        f"{'✅' if ok_ab else '❌'} Alts/Baixos ({len(bajos)}B/{6-len(bajos)}A)",
        f"{'✅' if (g_count==1 if con_gem else g_count==0) else '❌'} Bessons",
        f"{'✅' if (c_count==1 if con_cons else c_count==0) else '❌'} Consecutius"
    ]

# --- UI ---
st.title("PRIMITIVA PRO v7")
sorteigs, bote = obtenir_dades_reals()

st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote}</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Últims 3 Sorteigs")
for s in sorteigs:
    diag_list = detall_diagnostic(s['nums'], True, True)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <div style="font-weight:bold; border-bottom:1px solid black; margin-bottom:5px;">📅 {s['data']}</div>
            {n_html} <div class="num r-num">{s['r']}</div>
            <div style="margin-top:10px; background:#f9f9f9; padding:5px;">
                {"".join([f'<span class="diag-item">{item}</span>' for item in diag_list])}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("### Configuració")
gem_on = st.radio("Filtre Bessons", ["OFF", "ON"], index=1, key="g1") == "ON"
cons_on = st.radio("Filtre Consecutius", ["OFF", "ON"], index=1, key="c1") == "ON"

if st.button("GENERAR COMBINACIONS"):
    finales = []
    rs = [8, 5, 2, 0, 9, 3]
    intents = 0
    while len(finales) < 6 and intents < 50000:
        tipo_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 3) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 6:
            decs = [(x-1)//10 for x in c]
            if all(decs.count(i) <= 2 for i in range(5)): # FILTRE UNITATS (MÀX 2)
                if 131 <= sum(c) <= 160: # FILTRE SUMA
                    bajos = [x for x in c if x <= 25]
                    if (tipo_ab == "4B3A" and len(bajos) == 4) or (tipo_ab == "3B4A" and len(bajos) == 3):
                        g_count = len([x for x in c if x in gemelos_list])
                        if (gem_on and g_count == 1) or (not gem_on and g_count == 0):
                            sc = sorted(c)
                            cc = sum(1 for i in range(5) if sc[i+1]-sc[i] == 1)
                            if (cons_on and cc == 1) or (not cons_on and cc == 0):
                                finales.append(c)
        intents += 1
    
    if len(finales) < 6:
        st.warning("Filtres molt estrictes. Torna a intentar-ho.")
    else:
        st.subheader("Les teves Apostes")
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)

st.divider()
st.caption("Filtres: Màx 2 números/desena | Suma 131-160 | Alternança A/B")
