import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Primitiva P", page_icon="P")

# Estilo ultra-minimalista funcional
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 10px; border-radius: 8px; text-align: center; }
    .num { display: inline-block; width: 35px; height: 35px; line-height: 35px; border-radius: 50%; border: 1.5px solid black; margin: 4px; font-weight: bold; }
    .r-num { background-color: black; color: white; }
    button { background-color: black !important; color: white !important; border-radius: 0px !important; width: 100%; height: 50px; font-weight: bold; }
    /* Ajuste para que los radio se vean como botones limpios */
    div[data-testid="stRadio"] label { font-weight: bold; border: 1px solid #eee; padding: 5px 20px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# Listas de números (Lógica de grupos integrada)
n = list(range(1, 50))
desp = random.sample(n, 15)
hielo = random.sample(n, 12)
cal = random.sample(n, 10)
gemelos_list = [11, 22, 33, 44]

def validar_final(combo, anteriores, con_gem, con_cons, tipo):
    # Filtro Decenas 2-2-1-1-1
    decs = [(x-1)//10 for x in combo]
    if any(decs.count(i) == 0 for i in range(5)) or any(decs.count(i) > 2 for i in range(5)): return False
    # Filtro Suma
    if not (131 <= sum(combo) <= 160): return False
    # Filtro Altos/Bajos
    if len([x for x in combo if x <= 25]) != 4: return False
    # Filtro Pares
    pares = len([x for x in combo if x % 2 == 0])
    if (tipo == "3P4I" and pares != 3) or (tipo == "4P3I" and pares != 4): return False
    # Filtro Solapamiento (Máx 2 iguales)
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
    # Gemelos
    g_count = len([x for x in combo if x in gemelos_list])
    if con_gem and g_count != 1: return False
    if not con_gem and g_count > 0: return False
    # Consecutivos
    s = sorted(combo)
    c_count = sum(1 for idx in range(6) if s[idx+1]-s[idx] == 1)
    if con_cons and c_count != 1: return False
    if not con_cons and c_count > 0: return False
    return True

# --- INTERFAZ ---
st.title("P - PRIMITIVA")
st.write(f"Último Sorteo: {datetime.now().strftime('%d/%m/%Y')} | 02-15-26-33-41-48 R: 5")

# Botones de control (ahora visibles en móvil)
gem_on = st.radio("GEMELOS", ["OFF", "ON"], horizontal=True) == "ON"
cons_on = st.radio("CONSECUTIVOS", ["OFF", "ON"], horizontal=True) == "ON"

if st.button("GENERAR COMBINACIONES"):
    finales = []
    rs = random.sample(range(10), 6)
    
    intentos = 0
    while len(finales) < 6 and intentos < 15000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        # Regla: Máximo 3 combinaciones con el extra activado
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        # Generación base 4-2-1
        c = random.sample(desp, 4) + random.sample(hielo, 2) + [random.choice(cal)]
        c = list(set(c))
        
        if len(c) == 7 and validar_final(c, finales, usar_gem, usar_cons, tipo):
            finales.append(sorted(c))
        intentos += 1

    if len(finales) < 6:
        st.error("Los filtros son muy estrictos. Prueba a cambiar Gemelos/Consecutivos.")
    else:
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)
