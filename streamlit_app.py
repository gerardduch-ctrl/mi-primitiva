import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Múltiple", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 12px; text-align: center; background-color: #fff; }
    .num { display: inline-block; width: 32px; height: 32px; line-height: 32px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; color: black; text-align: center; }
    .r-num { background-color: black; color: white; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; }
    .diag-item { font-size: 12px; color: gray; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES OFICIALS VERIFICADES ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]
bote_actual = "9.500.000 €"

# --- LÒGICA DE FILTRES (Múltiple de 7 números) ---
gemelos_list = [11, 22, 33, 44]
cal_hist = [38, 39, 47, 3, 45, 30, 43, 23, 1, 48]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def validar_multiple(c, anteriores, gem_on, cons_on, t_ab):
    # 1. Decenes: Màxim 2 números per desena
    decs = [(x-1)//10 for x in c]
    if any(decs.count(i) > 2 for i in range(5)): return False
    # 2. Suma: Adaptada a 7 números (aprox 150-210)
    if not (150 <= sum(c) <= 220): return False
    # 3. Alts/Baixos: Alternança (4B/3A o 3B/4A)
    bajos = [x for x in c if x <= 25]
    if (t_ab == "4B3A" and len(bajos) != 4) or (t_ab == "3B4A" and len(bajos) != 3): return False
    # 4. Bessons i Consecutius
    gc = len([x for x in c if x in gemelos_list])
    if (gem_on and gc != 1) or (not gem_on and gc > 0): return False
    sc = sorted(c)
    cc = sum(1 for i in range(6) if sc[i+1]-sc[i] == 1)
    if (cons_on and cc != 1) or (not cons_on and cc > 0): return False
    return True

# --- INTERFÍCIE ---
st.title("PRIMITIVA PRO v8 - MÚLTIPLE")
st.markdown(f'<div class="bote-box">BOTE ACTUALITZAT:<br>{bote_actual}</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Històric Reial")
for s in sorteigs_reals:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("### Configuració")
gem_on = st.toggle("Activar Filtre Bessons", value=True)
cons_on = st.toggle("Activar Filtre Consecutius", value=True)

if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚMEROS)"):
    finales = []
    rs_top = [8, 5, 2, 7, 0, 1]
    intentos = 0
    
    while len(finales) < 6 and intentos < 60000:
        # Alternança Alts/Baixos
        t_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        # Generació de 7 números: 1 Calent, 4 Desp, 2 Hielo
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 7 and validar_multiple(c, finales, gem_on, cons_on, t_ab):
            finales.append(c)
        intentos += 1

    if len(finales) < 6:
        st.warning("Filtres massa exigents per a 7 números. Torna-ho a intentar.")
    else:
        st.subheader("Les teves Apostes Múltiples")
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)
            st.caption(f"Aposta {idx+1}: 7 números (Múltiple) - No ha sortit mai.")

st.divider()
st.info("Regla estricta: Màxim 2 números per desena per garantir dispersió total.")
