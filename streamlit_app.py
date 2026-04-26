import streamlit as st
import random
from itertools import combinations

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Ultra Speed", page_icon="P")

# CSS OPTIMITZAT: Minimalisme pur i negre forçat per a mòbil
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 11px; text-align: left; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CACHE DE DADES (Carrega en segons, guarda per sempre) ---
@st.cache_resource
def carregar_constants():
    return {
        "gemelos": {11, 22, 33, 44},
        "calientes": {3, 23, 30, 38, 39, 47},
        "historic": {frozenset({3, 6, 10, 28, 30, 46}), frozenset({11, 13, 20, 26, 27, 34}), frozenset({4, 7, 29, 39, 41, 48})}
    }

CONST = carregar_constants()

@st.cache_data(ttl=86400) # Guarda els resultats 24h
def dades_sorteigs():
    return [
        {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ], "9.500.000 €"

# --- LÒGICA DE DIAGNÒSTIC ---
def analitzar_v25(c):
    is_7 = len(c) == 7
    d = [(x-1)//10 for x in c]
    counts = sorted([d.count(i) for i in range(5)], reverse=True)
    target = [2, 2, 1, 1, 1] if is_7 else [2, 1, 1, 1, 1]
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    
    return [
        f"{'✅' if counts == target else '❌'} Decenes",
        f"{'✅' if l_inf <= s_tot <= l_sup else '❌'} Suma ({s_tot})",
        f"{'✅' if cc == 1 else '❌'} Consecutius"
    ]

# --- UI: ESTRUCTURE ---
sorteigs, bote = dades_sorteigs()
st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote}</div>', unsafe_allow_html=True)

for s in sorteigs:
    checks = analitzar_v25(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card"><strong>📅 {s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div><div class="diag-box">{" | ".join(checks)}</div></div>', unsafe_allow_html=True)

st.divider()

# FRAGMENT PER OPTIMITZAR ELS SELECTORS
@st.fragment
def panell_i_generador():
    st.subheader("⚙️ Configuració")
    f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
    f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
    f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
    gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
    cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)
    
    if st.button("GENERAR APOSTES ARA"):
        finales = []
        rs = [random.randint(0,4) for _ in range(3)] + [random.randint(5,9) for _ in range(3)]
        
        with st.status("💎 Optimitzant...", expanded=False):
            intents = 0
            while len(finales) < 6 and intents < 80000:
                idx = len(finales)
                c = sorted(random.sample(list(CONST["calientes"]), 1) + random.sample(range(1,50), 6))
                if len(set(c)) != 7: continue
                
                # Bessons i Consecutius
                gc = len([x for x in c if x in CONST["gemelos"]])
                cc = sum(1 for i in range(6) if c[i+1]-c[i] == 1)
                
                u_gem = gem_on if idx < 3 else False
                u_cons = cons_on if idx in [0, 2, 4] else False
                
                if (u_gem and gc != 1) or (not u_gem and gc > 0): continue
                if (u_cons and cc != 1) or (not u_cons and cc > 0): continue
                
                # Solapament màx 2
                if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
                
                finales.append(c)
                intents += 1
        
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)

panell_i_generador()
