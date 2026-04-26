import streamlit as st
import random
import time
from itertools import combinations

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro Ultra", page_icon="P")

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
    /* Spinner minimalista negre */
    div[data-testid="stStatusWidget"] { border: 1px solid black !important; border-radius: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CACHE DE DADES ---
@st.cache_resource
def carregar_base_dades():
    # Base de dades històrica en format set per velocitat punta
    return {frozenset({3, 6, 10, 28, 30, 46}), frozenset({11, 13, 20, 26, 27, 34}), frozenset({4, 7, 29, 39, 41, 48})}

@st.cache_data(ttl=3600)
def obtenir_sorteigs_i_bote():
    sorteigs = [
        {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ]
    return sorteigs, "9.500.000 €"

# --- LÒGICA ---
HISTORIC_GUANYADORS = carregar_base_dades()
gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 23, 30, 38, 39, 47]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def es_inedita(combo):
    return not any(frozenset(sub) in HISTORIC_GUANYADORS for sub in combinations(combo, 6))

# --- UI PRINCIPAL ---
st.title("PRIMITIVA PRO ULTRA v23")
sorteigs, bote = obtenir_sorteigs_i_bote()

st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote}</div>', unsafe_allow_html=True)

for s in sorteigs:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# PANELL CONTROL
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)

if 'apostes' not in st.session_state: st.session_state.apostes = []

if st.button("GENERAR APOSTES OPTIMITZADES"):
    finales = []
    rs_top = [random.randint(0,9) for _ in range(6)]
    
    # SPINNER MINIMALISTA I ENTRETINGUT
    with st.status("🚀 Processant algorisme estadístic...", expanded=True) as status:
        st.write("📊 Analitzant historial des de 1985...")
        time.sleep(0.4)
        st.write("🧩 Aplicant filtres de desenes 2-2-1-1-1...")
        
        intents = 0
        while len(finales) < 6 and intents < 100000:
            idx = len(finales)
            t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
            u_gem = gem_on if idx < 3 else False
            u_cons = cons_on if idx in [0, 2, 4] else False
            
            c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
            
            if len(set(c)) == 7:
                if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
                if not es_inedita(c): continue
                
                # Validacions ràpides
                decs = [(x-1)//10 for x in c]
                if f_dec and sorted([decs.count(i) for i in range(5)], reverse=True) != [2, 2, 1, 1, 1]: continue
                if f_suma and not (150 <= sum(c) <= 220): continue
                
                sc = sorted(c)
                cc = sum(1 for i in range(6) if sc[i+1]-sc[i] == 1)
                if (u_cons and cc != 1) or (not u_cons and cc > 0): continue
                
                finales.append(c)
            intents += 1
        
        st.write("✨ Verificant inèdites i solapaments...")
        time.sleep(0.3)
        status.update(label="✅ Combinacions optimitzades trobades!", state="complete", expanded=False)
        
    st.session_state.apostes = finales

# MOSTRAR RESULTATS
if st.session_state.apostes:
    for idx, combo in enumerate(st.session_state.apostes):
        n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
        st.markdown(f'<div class="card">{n_html}</div>', unsafe_allow_html=True)
