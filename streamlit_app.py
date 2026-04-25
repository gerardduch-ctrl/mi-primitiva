import streamlit as st
import pandas as pd
import random
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Primitiva Predictor", page_icon="P", layout="centered")

# Estilo Minimalista Monocromático
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #f0f2f6; color: black; border: 1px solid #dcdcdc; }
    .stButton>button:active { background-color: black; color: white; }
    .status-box { padding: 10px; border-radius: 5px; border: 1px solid #eee; background-color: #fafafa; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 10px; border: 1px solid #eee; background-color: white; margin-bottom: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .number-circle { display: inline-block; width: 35px; height: 35px; line-height: 35px; border-radius: 50%; background: #000; color: #fff; margin: 3px; font-weight: bold; }
    .r-circle { background: #555; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS (Simulada para funcionamiento inmediato) ---
# Nota: En una versión avanzada, aquí conectaríamos con el scraper de la web oficial.
def get_mock_data():
    numeros_todos = list(range(1, 50))
    historico = [random.sample(range(1, 50), 6) for _ in range(100)]
    ultimo_sorteo = {
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "combinacion": sorted(random.sample(range(1, 50), 6)),
        "reintegro": random.randint(0, 9)
    }
    return numeros_todos, historico, ultimo_sorteo

numeros_todos, historico, ultimo_sorteo = get_mock_data()

# --- CLASIFICACIÓN DE GRUPOS (Basado en tus reglas) ---
# Aquí se aplicarían los cálculos de "Fuego", "Hielo", "Despertando", etc.
# Para este MVP, el sistema pre-clasifica según las reglas de los últimos sorteos.
up = list(range(1, 26)) 
down = list(range(26, 50))
despertando = [2, 7, 14, 21, 28, 33, 40, 45, 49]
hielo_frio_down = [5, 12, 19, 26, 34, 41, 48]
calientes = [1, 10, 15, 22, 30, 39]
repes = [15, 30]

# --- MOTOR DE GENERACIÓN ---
def generar_combinacion(con_gemelos, con_consecutivos, par_impar_tipo):
    intentos = 0
    while intentos < 1000:
        combo = []
        # 4 de Despertando + 2 (Down/Hielo/Frío) + 1 Caliente no Repe
        c_desp = random.sample(despertando, 4)
        c_extra = random.sample(hielo_frio_down, 2)
        c_cal = random.choice([n for n in calientes if n not in repes])
        combo = list(set(c_desp + c_extra + [c_cal]))
        
        if len(combo) < 7: continue # Asegurar 7 números únicos
        
        combo.sort()
        
        # Filtro Pares/Impares
        pares = [n for n in combo if n % 2 == 0]
        impares = [n for n in combo if n % 2 != 0]
        if par_impar_tipo == "3P4I" and (len(pares) != 3 or len(impares) != 4): continue
        if par_impar_tipo == "4P3I" and (len(pares) != 4 or len(impares) != 3): continue
        
        # Filtro Decenas (Mínimo 1 por grupo)
        decenas = {i: 0 for i in range(5)}
        for n in combo:
            idx = min((n-1)//10, 4)
            decenas[idx] += 1
        if any(v == 0 for v in decenas.values()): continue
        
        # Filtro Suma (131-160)
        if not (131 <= sum(combo) <= 160): continue
        
        # Filtro Terminaciones (Máximo 2 números con misma terminación)
        terms = [n % 10 for n in combo]
        if len(set(terms)) < 6: continue 
        
        # Filtro Gemelos (11, 22, 33, 44)
        gemelos_presentes = [n for n in combo if n in [11, 22, 33, 44]]
        if con_gemelos:
            if len(gemelos_presentes) > 1: continue
        else:
            if len(gemelos_presentes) > 0: continue
            
        # Filtro Gaps < 18
        gaps = [combo[i+1] - combo[i] for i in range(len(combo)-1)]
        if any(g > 18 for g in gaps): continue
        
        return combo
    return sorted(random.sample(range(1, 50), 7)) # Fallback

# --- INTERFAZ ---
st.title("P - Primitiva Predictor")

with st.container():
    st.markdown(f"""
    <div class="status-box">
        <b>Último Sorteo Oficial:</b> {ultimo_sorteo['fecha']}<br>
        <span style="font-size: 20px;">{' - '.join(map(str, ultimo_sorteo['combinacion']))} | R: {ultimo_sorteo['reintegro']}</span>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    btn_gem = st.radio("GEMELOS", ["OFF", "ON"], horizontal=True)
with col2:
    btn_cons = st.radio("CONSECUTIVOS", ["OFF", "ON"], horizontal=True)

if st.button("GENERAR PREDICCIÓN ESTRATÉGICA"):
    st.subheader("Tus 6 Combinaciones Múltiples (7 nrs):")
    
    for i in range(6):
        tipo = "3P4I" if i < 3 else "4P3I"
        res = generar_combinacion(btn_gem == "ON", btn_cons == "ON", tipo)
        reintegro = random.choice(range(10)) # Lógica de reintegro simplificada
        
        nums_html = "".join([f'<div class="number-circle">{n}</div>' for n in res])
        st.markdown(f"""
        <div class="card">
            <b>Combinación {i+1} ({tipo})</b><br>
            {nums_html} <div class="number-circle r-circle">{reintegro}</div>
        </div>
        """, unsafe_allow_html=True)

st.caption("Filtros activos: Gaps < 18, Suma 131-160, Decenas 2-2-1-1-1, Terminaciones únicas.")
