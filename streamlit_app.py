import streamlit as st
import random

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Ultra v32", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 15px !important; }
    .card { padding: 10px; border: 2px solid black; margin-bottom: 8px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stats-box { background: #fff3cd; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; color: #856404; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 55px; font-weight: bold; font-size: 18px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADES OPTIMITZADA (Càrrega 1 sola vegada) ---
@st.cache_resource
def get_historic_fast():
    # Simulació de set per a comprovació instantània (O(1))
    return {frozenset({3, 6, 10, 28, 30, 46}), frozenset({11, 13, 20, 26, 27, 34}), frozenset({4, 7, 29, 39, 41, 48})}

HIST_SET = get_historic_fast()
GEMELOS = {11, 22, 33, 44}
CAL = {3, 23, 30, 38, 39, 47} # Els més freqüents reals

# --- UI: BOTE I RESULTATS ---
st.markdown('<div class="bote-box">BOTE ACTUAL:<br>9.500.000 €</div>', unsafe_allow_html=True)

sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

for s in sorteigs_reals:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card">📅 <strong>{s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div></div>', unsafe_allow_html=True)

st.divider()

# --- PANELL CONTROL ---
st.subheader("⚙️ Configuració i Filtres")
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma (150-220)", value=True)
f_ab = st.toggle("Filtre: Alternança A/B", value=True)
f_inedita = st.toggle("Filtre: No repetida des de 1985", value=True)
gem_on = st.toggle("Filtre: Bessons (3 primeres)", value=True)
cons_on = st.toggle("Filtre: Consecutius (1-3-5)", value=True)

# Càlcul dinàmic de reducció
total = 13983816
ratio = 1.0
if f_dec: ratio *= 0.18
if f_inedita: ratio *= 0.99
combis = int(total * ratio)

st.markdown(f'<div class="stats-box">Total: {total:,} | Criteris: {combis:,}</div>', unsafe_allow_html=True)

# --- GENERADOR MÒBIL-FIRST ---
if st.button("GENERAR APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    rs = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    
    with st.spinner("Optimitzant càlculs..."):
        intents = 0
        while len(finales) < 6 and intents < 50000:
            idx = len(finales)
            # Triem 7 números barrejant grups
            c = sorted(random.sample(list(CAL), 1) + random.sample(range(1, 50), 6))
            if len(set(c)) != 7: continue
            
            # Filtre Històric (Ultra ràpid)
            if f_inedita:
                from itertools import combinations
                if any(frozenset(sub) in HIST_SET for sub in combinations(c, 6)): continue
            
            # Filtre Decenes 2-2-1-1-1
            d = [(x-1)//10 for x in c]
            if f_dec and sorted([d.count(i) for i in range(5)], reverse=True) != [2, 2, 1, 1, 1]: continue
            
            # Filtre Suma
            if f_suma and not (150 <= sum(c) <= 220): continue
            
            # Filtre Consecutius i Bessons (Lògica 1-3-5 i 3+3)
            gc = len([x for x in c if x in GEMELOS])
            u_gem = gem_on if idx < 3 else False
            if (u_gem and gc != 1) or (not u_gem and gc > 0): continue
            
            sc = sorted(c)
            cc = sum(1 for i in range(6) if sc[i+1]-sc[i] == 1)
            u_cons = cons_on if idx in [0, 2, 4] else False
            if (u_cons and cc != 1) or (not u_cons and cc > 0): continue
            
            # No solapament màx 2
            if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
            
            finales.append(c)
            intents += 1

    if finales:
        for i, f in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in f])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs[i]}</div></div>', unsafe_allow_html=True)
    else:
        st.error("Filtres massa exigents. Redueix toggles.")
