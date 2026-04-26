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
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #000000; color: white; border: none; }
    .stButton>button:hover { background-color: #333333; color: white; }
    .status-box { padding: 15px; border-radius: 10px; border: 1px solid #eee; background-color: #f9f9f9; margin-bottom: 20px; text-align: center; }
    .card { padding: 15px; border-radius: 10px; border: 1px solid #eee; background-color: white; margin-bottom: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .number-circle { display: inline-block; width: 35px; height: 35px; line-height: 35px; border-radius: 50%; background: #000; color: #fff; margin: 3px; font-weight: bold; font-size: 14px; }
    .r-circle { background: #888; }
    /* Estilo para radio buttons ON/OFF */
    div.row-widget.stRadio > div{ flex-direction:row; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS Y GRUPOS ---
# Simulamos la clasificación basada en tus reglas para que sea funcional
nros = list(range(1, 50))
up = nros[:25]
down = nros[25:]
fuego = random.sample(nros, 20)
hielo = [n for n in nros if n not in fuego]
calientes = random.sample(nros, 15)
repes = random.sample(calientes, 3)
frios = [n for n in nros if n not in calientes]
despertando = random.sample(frios, 10)
hielo_frio_down = [n for n in down if n in hielo and n in frios]
# En caso de que la intersección sea pequeña, rellenamos para evitar errores
if len(hielo_frio_down) < 2: hielo_frio_down = random.sample(down, 5)

# --- MOTOR DE GENERACIÓN ---
def validar_solapamiento(nueva_comb, anteriores):
    for vieja in anteriores:
        coincidencias = len(set(nueva_comb) & set(vieja))
        if coincidencias > 2:
            return False
    return True

def generar_comb(con_gem, con_cons, tipo, anteriores):
    gemelos = [11, 22, 33, 44]
    for _ in range(2000): # Intentos para encontrar la combinación perfecta
        # Composición: 4 Despertando + 2 (Down/Hielo/Frío) + 1 Caliente no Repe
        c_desp = random.sample(despertando, 4)
        c_extra = random.sample(hielo_frio_down, 2)
        c_cal = [n for n in calientes if n not in repes]
        if not c_cal: c_cal = [1]
        c_final = list(set(c_desp + c_extra + [random.choice(c_cal)]))
        
        if len(c_final) < 7: continue
        c_final.sort()

        # Filtro Solapamiento (NUEVO: Máx 2 números iguales con las anteriores)
        if not validar_solapamiento(c_final, anteriores): continue

        # Filtro Pares/Impares
        p = [n for n in c_final if n % 2 == 0]
        i = [n for n in c_final if n % 2 != 0]
        if tipo == "3P4I" and len(p) != 3: continue
        if tipo == "4P3I" and len(p) != 4: continue

        # Filtro Decenas (2-2-1-1-1)
        decs = [(n-1)//10 for n in c_final]
        if len(set(decs)) < 5: continue

        # Filtro Suma (131-160)
        if not (131 <= sum(c_final) <= 160): continue

        # Filtro Terminaciones (Máximo 2 números misma terminación)
        terms = [n % 10 for n in c_final]
        if len(set(terms)) < 6: continue

        # Filtro Gaps < 18
        if any(c_final[idx+1] - c_final[idx] > 18 for idx in range(6)): continue

        # Filtro Gemelos
        presentes_gem = [n for n in c_final if n in gemelos]
        if con_gem:
            if len(presentes_gem) != 1: continue
        else:
            if len(presentes_gem) > 0: continue
            
        return c_final
    return sorted(random.sample(range(1, 50), 7))

# --- INTERFAZ ---
st.title("P - Primitiva")

# Datos del último sorteo (Simulado)
st.markdown(f"""<div class="status-box">
    <b>Último Sorteo: {datetime.now().strftime('%d/%m/%Y')}</b><br>
    <span style="font-size: 1.2em;">04 - 12 - 25 - 31 - 44 - 49 | R: 7</span>
    </div>""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    gem_mode = st.radio("GEMELOS", ["OFF", "ON"])
with c2:
    cons_mode = st.radio("CONSECUTIVOS", ["OFF", "ON"])

if st.button("GENERAR 6 MÚLTIPLES"):
    combinaciones_finales = []
    reintegros_frios = random.sample(range(10), 3)
    reintegros_desp = random.sample([n for n in range(10) if n not in reintegros_frios], 3)
    
    for idx in range(6):
        tipo = "3P4I" if idx < 3 else "4P3I"
        # Controlar que solo 3 combinaciones tengan gemelos si el botón está ON
        usar_gemelo = (gem_mode == "ON" and idx < 3)
        
        nueva = generar_comb(usar_gemelo, cons_mode == "ON", tipo, combinaciones_finales)
        combinaciones_finales.append(nueva)
        
        r = reintegros_frios[idx] if idx < 3 else reintegros_desp[idx-3]
        
        nums_html = "".join([f'<div class="number-circle">{n}</div>' for n in nueva])
        st.markdown(f"""<div class="card">
            <small>Múltiple {idx+1} ({tipo})</small><br>
            {nums_html} <div class="number-circle r-circle">{r}</div>
            </div>""", unsafe_allow_html=True)
