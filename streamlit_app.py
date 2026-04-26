import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Primitiva Predictor", page_icon="P", layout="centered")

# CSS para estilo minimalista monocromático
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .stButton>button { width: 100%; border-radius: 0px; height: 3.5em; background-color: black; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #333; }
    .card { padding: 20px; border: 1px solid #000; margin-bottom: 15px; text-align: center; }
    .num { display: inline-block; width: 38px; height: 38px; line-height: 38px; border-radius: 50%; border: 1px solid #000; margin: 4px; font-weight: bold; font-size: 15px; }
    .r-num { background-color: #000; color: white; }
    div[data-testid="stRadio"] > div { flex-direction: row; gap: 20px; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE GRUPOS (Simbólica para ejecución) ---
n = list(range(1, 50))
despertando = random.sample(n, 12)
hielo_frio_down = random.sample(n, 10)
calientes = random.sample(n, 10)
repes = random.sample(calientes, 2)
gemelos_list = [11, 22, 33, 44]

# --- MOTOR DE VALIDACIÓN ---
def validar_todo(combo, anteriores, con_gem, con_cons, tipo):
    # 1. Decenas: 2-2-1-1-1 (Obligatorio)
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    if any(c == 0 for c in counts) or any(c > 2 for c in counts): return False
    
    # 2. Suma: 131-160
    if not (131 <= sum(combo) <= 160): return False
    
    # 3. Altos/Bajos: 4 (1-25) y 3 (26-49)
    bajos = [x for x in combo if x <= 25]
    if len(bajos) != 4: return False
    
    # 4. Pares/Impares
    pares = [x for x in combo if x % 2 == 0]
    if tipo == "3P4I" and len(pares) != 3: return False
    if tipo == "4P3I" and len(pares) != 4: return False
    
    # 5. Terminaciones: Solo 1 repetida (máx 2 veces)
    terms = [x % 10 for x in combo]
    if len(set(terms)) != 6: return False
    
    # 6. Solapamiento: Máx 2 números iguales con previas
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
        
    # 7. Gemelos y Consecutivos (Lógica de Botones)
    pres_gem = [x for x in combo if x in gemelos_list]
    if con_gem and len(pres_gem) != 1: return False
    if not con_gem and len(pres_gem) > 0: return False
    
    sorted_c = sorted(combo)
    diffs = [sorted_c[i+1]-sorted_c[i] for i in range(len(sorted_c)-1)]
    if any(d > 18 for d in diffs): return False # Gap < 18
    
    has_cons = diffs.count(1)
    if con_cons and has_cons != 1: return False # Exactamente una pareja
    if not con_cons and has_cons > 0: return False
    
    return True

# --- INTERFAZ ---
st.title("P - PRIMITIVA")
st.write(f"Último Sorteo: {datetime.now().strftime('%d/%m/%Y')} | 05-14-22-38-41-47 R: 3")

col1, col2 = st.columns(2)
with col1: gem_on = st.radio("GEMELOS", ["OFF", "ON"]) == "ON"
with col2: cons_on = st.radio("CONSECUTIVOS", ["OFF", "ON"]) == "ON"

if st.button("GENERAR"):
    finales = []
    # Reintegros: 3 Fríos, 3 Despertando
    rs = random.sample(range(10), 6) 
    
    intentos_totales = 0
    while len(finales) < 6 and intentos_totales < 10000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        # Aplicar límite de 3 combinaciones con gemelos/consecutivos si el botón está ON
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        # Selección base
        c = random.sample(despertando, 4) + random.sample(hielo_frio_down, 2) + [random.choice(calientes)]
        c = list(set(c))
        
        if len(c) == 7 and validar_todo(c, finales, usar_gem, usar_cons, tipo):
            finales.append(sorted(c))
        intentos_totales += 1

    for idx, combo in enumerate(finales):
        html = "".join([f'<div class="num">{n}</div>' for n in combo])
        st.markdown(f'<div class="card">{html}<div class="num r-num">{rs[idx]}</div></div>', unsafe_allow_html=True)
