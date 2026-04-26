import streamlit as st
import random
import requests
from bs4 import BeautifulSoup

# --- 1. CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Pro v30", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 14px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; line-height: 1.5; color: #333; font-weight: bold; text-align: left; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stats-box { background-color: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; margin: 15px 0; font-family: monospace; font-size: 12px; color: #856404; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADES REALS I GRUPS ---
if 'sorteigs' not in st.session_state:
    st.session_state.sorteigs = [
        {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ]
    st.session_state.bote = "9.500.000 €"

gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 23, 30, 38, 39, 47, 45, 10, 11, 49]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

# --- 3. FUNCIONS DE CÀLCUL ---
def analitzar_total(c):
    is_7 = len(c) == 7
    d = [(x-1)//10 for x in c]
    counts = sorted([d.count(i) for i in range(5)], reverse=True)
    target = [2, 2, 1, 1, 1] if is_7 else [2, 1, 1, 1, 1]
    
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in gemelos_list])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    terms = [x % 10 for x in c]
    ok_t = all(terms.count(i) <= 2 for i in range(10))

    return {
        "Dec": counts == target,
        "Sum": l_inf <= s_tot <= l_sup,
        "AB": bajos in [3, 4],
        "PS": pares in [3, 4],
        "Bes": gc == 1,
        "Cons": cc == 1,
        "Term": ok_t,
        "val_sum": s_tot,
        "val_ab": f"{bajos}B",
        "val_ps": f"{pares}P"
    }

# --- UI: BOTE I HISTÒRIC ---
st.markdown(f'<div class="bote-box">BOTE ACTUAL:<br>{st.session_state.bote}</div>', unsafe_allow_html=True)

st.subheader("Diagnòstic dels 3 Últims Sorteigs")
for s in st.session_state.sorteigs:
    res = analitzar_total(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">
                {'✅' if res['Dec'] else '❌'} Decenes | {'✅' if res['Sum'] else '❌'} Suma ({res['val_sum']}) | 
                {'✅' if res['AB'] else '❌'} A/B ({res['val_ab']}) | {'✅' if res['PS'] else '❌'} P/S ({res['val_ps']}) |
                {'✅' if res['Bes'] else '❌'} Bessons | {'✅' if res['Cons'] else '❌'} Cons | 
                {'✅' if res['Term'] else '❌'} Terminacions
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- UI: PANELL DE CONTROL ---
st.subheader("⚙️ Filtres i Reducció d'Apostes Simples")
f_dec = st.toggle("Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Suma equilibrada", value=True)
f_ab = st.toggle("Alts/Baixos (4/3)", value=True)
f_ps = st.toggle("Parells/Senars (4/3)", value=True)
gem_on = st.toggle("Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Consecutius (Apostes 1, 3, 5)", value=True)
f_term = st.toggle("Terminacions (Màx 2)", value=True)

# --- CÀLCUL MATEMÀTIC DE REDUCCIÓ ---
total = 13983816
restant = total
if f_dec: restant *= 0.18  # Reducció per dispersió de desenes
if f_suma: restant *= 0.15 # Rang central de la campana de Gauss
if f_ab: restant *= 0.35   # Proporció 3:3 o 4:2
if f_ps: restant *= 0.35   # Proporció 3:3 o 4:2
if gem_on: restant *= 0.12 # Probabilitat d'un bessó exacte
if cons_on: restant *= 0.40# Probabilitat d'una parella consecutiva
if f_term: restant *= 0.85 # Probabilitat de no repetir terminacions

st.markdown(f"""
    <div class="stats-box">
        TOTAL APOSTES SIMPLES: {total:,}<br>
        APOSTES QUE COMPLEIXEN ELS FILTRES: {int(restant):,}<br>
        EFICIÈNCIA DEL SISTEMA: {((total - restant) / total * 100):.2f}% de descart
    </div>
""", unsafe_allow_html=True)

# --- GENERADOR (7 NÚMEROS) ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES OPTIMITZADES"):
    finales = []
    rs_orig = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    intents = 0
    while len(finales) < 6 and intents < 80000:
        idx = len(finales)
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        
        c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
        
        if len(set(c)) == 7:
            res = analitzar_total(c)
            # Validació estricta segons toggles
            if f_dec and not res['Dec']: continue
            if f_suma and not res['Sum']: continue
            if f_ab and not (len([x for x in c if x<=25]) == (4 if t_ab=="4B3A" else 3)): continue
            if f_ps and not (len([x for x in c if x%2==0]) == (4 if t_ps=="4P3S" else 3)): continue
            if (u_gem and not res['Bes']) or (not u_gem and res['Bes']): continue
            if (u_cons and not res['Cons']) or (not u_cons and res['Cons']): continue
            if f_term and not res['Term']: continue
            if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
            
            finales.append(c)
        intents += 1

    if finales:
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs_orig[i]}</div></div>', unsafe_allow_html=True)
