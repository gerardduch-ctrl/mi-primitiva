import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva", page_icon="P")

# Estil minimalista corregit per a mòbils
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 12px; border-radius: 5px; text-align: center; background-color: #fff; }
    .num { display: inline-block; width: 34px; height: 34px; line-height: 34px; border-radius: 50%; border: 1.5px solid black; margin: 3px; font-weight: bold; font-size: 14px; color: black; }
    .r-num { background-color: black; color: white; }
    .stButton>button { background-color: black !important; color: white !important; border: none; width: 100%; height: 50px; font-weight: bold; border-radius: 0px; margin-top: 20px; }
    /* Etiquetes dels selectors més visibles */
    label { font-size: 18px !important; font-weight: bold !important; color: black !important; display: block; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Lògica de grups (perquè el codi funcioni immediatament)
n = list(range(1, 50))
desp = random.sample(n, 18)
hielo = random.sample(n, 12)
cal = random.sample(n, 8)
gemelos_list = [11, 22, 33, 44]

def validar_final(combo, anteriores, con_gem, con_cons, tipo):
    # 1. Decenes 2-2-1-1-1
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    if any(c == 0 for c in counts) or any(c > 2 for c in counts): return False
    # 2. Suma 131-160
    if not (131 <= sum(combo) <= 160): return False
    # 3. Alts/Baixos 4/3
    if len([x for x in combo if x <= 25]) != 4: return False
    # 4. Parells/Senars
    p_count = len([x for x in combo if x % 2 == 0])
    if (tipo == "3P4I" and p_count != 3) or (tipo == "4P3I" and p_count != 4): return False
    # 5. Solapament Máx 2
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
    # 6. Gemelos
    g_count = len([x for x in combo if x in gemelos_list])
    if con_gem and g_count != 1: return False
    if not con_gem and g_count > 0: return False
    # 7. Consecutius
    s = sorted(combo)
    c_count = sum(1 for i in range(6) if s[i+1]-s[i] == 1)
    if con_cons and c_count != 1: return False
    if not con_cons and c_count > 0: return False
    return True

# --- INTERFÍCIE ---
st.title("PRIMITIVA")
st.write(f"Últim Sorteig: {datetime.now().strftime('%d/%m/%Y')} | 05-18-21-34-40-44 R: 2")

st.divider() # Línia de separació

# Selectors clarament etiquetats
gem_on = st.radio("11, 22, 33, 44", ["OFF", "ON"], horizontal=True) == "ON"
st.write("") # Espai buit
cons_on = st.radio("CONSECUTIUS", ["OFF", "ON"], horizontal=True) == "ON"

if st.button("GENERAR COMBINACIONS"):
    finales = []
    rs = random.sample(range(10), 6)
    
    intentos = 0
    while len(finales) < 6 and intentos < 25000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        c = random.sample(desp, 4) + random.sample(hielo, 2) + [random.choice(cal)]
        c = list(set(c))
        
        if len(c) == 7 and validar_final(c, finales, usar_gem, usar_cons, tipo):
            finales.append(sorted(c))
        intentos += 1

    if len(finales) < 6:
        st.warning("Filtres massa estrictes. Torna-ho a provar.")
    else:
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)
