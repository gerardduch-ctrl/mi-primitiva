import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva", page_icon="P")

# CSS per forçar el color NEGRE i el minimalisme
st.markdown("""
    <style>
    /* Fons blanc i lletra negra */
    .stApp { background-color: white; color: black; }
    
    /* Estil de les boles de números */
    .card { padding: 15px; border: 2px solid black; margin-bottom: 12px; text-align: center; background-color: #fff; }
    .num { display: inline-block; width: 32px; height: 32px; line-height: 32px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; color: black; }
    .r-num { background-color: black; color: white; }
    
    /* Botó GENERAR en Negre */
    .stButton>button { background-color: black !important; color: white !important; border: none; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; }
    
    /* Títols dels selectors */
    .tit-selector { font-size: 20px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid black; display: inline-block; width: 100%; }
    
    /* Forçar que el botó de ràdio es vegi */
    div[data-testid="stRadio"] label { font-size: 22px !important; font-weight: bold !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# Lògica interna (Grups de números)
n = list(range(1, 50))
desp = random.sample(n, 20)
hielo = random.sample(n, 15)
cal = random.sample(n, 10)
gemelos_list = [11, 22, 33, 44]

def validar_final(combo, anteriores, con_gem, con_cons, tipo):
    # Decenes 2-2-1-1-1
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    if any(c == 0 for c in counts) or any(c > 2 for c in counts): return False
    # Suma 131-160
    if not (131 <= sum(combo) <= 160): return False
    # Alts/Baixos 4/3
    if len([x for x in combo if x <= 25]) != 4: return False
    # Parells/Senars
    p_count = len([x for x in combo if x % 2 == 0])
    if (tipo == "3P4I" and p_count != 3) or (tipo == "4P3I" and p_count != 4): return False
    # Solapament Máx 2
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
    # Gemelos
    g_count = len([x for x in combo if x in gemelos_list])
    if con_gem and g_count != 1: return False
    if not con_gem and g_count > 0: return False
    # Consecutius
    s = sorted(combo)
    c_count = sum(1 for i in range(6) if s[i+1]-s[i] == 1)
    if con_cons and c_count != 1: return False
    if not con_cons and c_count > 0: return False
    return True

# --- INTERFÍCIE ---
st.title("P - PRIMITIVA")
st.write(f"Sorteig: {datetime.now().strftime('%d/%m/%Y')} | 08-14-23-35-42-49 R: 9")

# SELECTORS ON/OFF (Dissenyats per ser visibles al mòbil)
st.markdown('<p class="tit-selector">NÚMEROS GEMELOS</p>', unsafe_allow_html=True)
gem_on = st.radio("Gemelos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

st.markdown('<p class="tit-selector">NÚMEROS CONSECUTIVOS</p>', unsafe_allow_html=True)
cons_on = st.radio("Consecutivos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

if st.button("GENERAR COMBINACIONS"):
    finales = []
    rs = random.sample(range(10), 6)
    
    intentos = 0
    while len(finales) < 6 and intentos < 30000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        c = random.sample(desp, 4) + random.sample(hielo, 2) + [random.choice(cal)]
        c = list(set(c))
        
        if len(c) == 7 and validar_final(c, finales, usar_gem, usar_cons, tipo):
            finales.append(sorted(c))
        intentos += 1

    if len(finales) < 6:
        st.warning("Filtres molt estrictes. Torna-ho a provar.")
    else:
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)
