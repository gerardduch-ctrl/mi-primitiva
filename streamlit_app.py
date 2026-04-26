import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva", page_icon="P")

# CSS per forçar NEGRETA, COLOR NEGRE i minimalisme total
st.markdown("""
    <style>
    /* Fons blanc i text general negre */
    .stApp { background-color: white; color: black; }
    
    /* Estil de les boles de números */
    .card { padding: 15px; border: 2px solid black; margin-bottom: 12px; text-align: center; background-color: #fff; }
    .num { display: inline-block; width: 32px; height: 32px; line-height: 32px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; color: black; }
    .r-num { background-color: black; color: white; }
    
    /* Botó GENERAR en Negre total */
    .stButton>button { background-color: black !important; color: white !important; border: none; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; }
    
    /* Títols dels selectors amb línia negra */
    .tit-selector { font-size: 18px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid black; display: inline-block; width: 100%; color: black; text-transform: uppercase; }
    
    /* FORÇAR ON/OFF EN NEGRE I NEGRETA */
    div[data-testid="stRadio"] label p {
        font-size: 20px !important;
        font-weight: 900 !important; /* Negreta màxima */
        color: black !important;     /* Negre pur */
        opacity: 1 !important;       /* Sense transparències */
    }
    
    /* Eliminar l'espai buit innecessari de Streamlit */
    div[data-testid="stVerticalBlock"] > div:has(div.tit-selector) {
        padding-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# Lògica interna (Grups de números simulats segons les teves regles)
n = list(range(1, 50))
desp = random.sample(n, 20)
hielo = random.sample(n, 15)
cal = random.sample(n, 10)
gemelos_list = [11, 22, 33, 44]

def validar_final(combo, anteriores, con_gem, con_cons, tipo):
    # 1. Decenes 2-2-1-1-1 (OBLIGATORI)
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    if any(c == 0 for c in counts) or any(c > 2 for c in counts): return False
    
    # 2. Suma 131-160
    if not (131 <= sum(combo) <= 160): return False
    
    # 3. Alts/Baixos: 4 (1-25) i 3 (26-49)
    bajos = [x for x in combo if x <= 25]
    if len(bajos) != 4: return False
    
    # 4. Parells/Senars
    p_count = len([x for x in combo if x % 2 == 0])
    if (tipo == "3P4I" and p_count != 3) or (tipo == "4P3I" and p_count != 4): return False
    
    # 5. Solapament Máx 2 números entre combinacions
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
    
    # 6. Gemelos (Lògica de botó)
    g_count = len([x for x in combo if x in gemelos_list])
    if con_gem and g_count != 1: return False
    if not con_gem and g_count > 0: return False
    
    # 7. Consecutius (Lògica de botó)
    s = sorted(combo)
    c_count = sum(1 for i in range(6) if s[i+1]-s[i] == 1)
    if con_cons and c_count != 1: return False
    if not con_cons and c_count > 0: return False
    
    return True

# --- INTERFÍCIE ---
st.title("PRIMITIVA")
st.write(f"Sorteig: {datetime.now().strftime('%d/%m/%Y')} | 08-14-23-35-42-49 R: 9")

# SELECTORS ON/OFF (Amb text forçat en negre i negreta)
st.markdown('<p class="tit-selector">NÚMEROS BESSONS</p>', unsafe_allow_html=True)
gem_on = st.radio("Gemelos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

st.markdown('<p class="tit-selector">NÚMEROS CONSECUTIUS</p>', unsafe_allow_html=True)
cons_on = st.radio("Consecutivos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

if st.button("GENERAR COMBINACIONS"):
    finales = []
    # Reintegres: 3 Frios, 3 Despertando
    rs = random.sample(range(10), 6)
    
    intentos = 0
    while len(finales) < 6 and intentos < 35000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        # Regla: Màxim 3 combinacions amb l'extra activat
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        # Generació base 4 Desp + 2 Hielo + 1 Cal
        c = random.sample(desp, 4) + random.sample(hielo, 2) + [random.choice(cal)]
        c = list(set(c))
        
        if len(c) == 7 and validar_final(c, finales, usar_gem, usar_cons, tipo):
            finales.append(sorted(c))
        intentos += 1

    if len(finales) < 6:
        st.warning("Filtres molt estrictes. Torna-ho a intentar.")
    else:
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)
