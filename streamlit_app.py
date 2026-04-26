import streamlit as st
import random

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Pro v15", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 38, 39, 47, 45]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def validar_estricte_v15(c, anteriores, f_dec, f_suma, f_ab, f_ps, f_term, usar_gem, usar_cons, t_ab, t_ps):
    # 1. DECENES 2-2-1-1-1 (LÒGICA ORIGINAL)
    if f_dec:
        decs = [(x-1)//10 for x in c]
        counts = sorted([decs.count(i) for i in range(5)], reverse=True)
        # Per a 7 números, el patró original de dispersió és [2, 2, 1, 1, 1]
        if counts != [2, 2, 1, 1, 1]: return False
    
    # 2. SUMA (150-220 per a 7 números)
    if f_suma and not (150 <= sum(c) <= 220): return False
    
    # 3. ALTS/BAIXOS
    bajos = [x for x in c if x <= 25]
    if f_ab and len(bajos) != (4 if t_ab == "4B3A" else 3): return False
    
    # 4. PARELLS/SENARS
    pares = len([x for x in c if x % 2 == 0])
    if f_ps and pares != (4 if t_ps == "4P3S" else 3): return False
    
    # 5. BESSONS
    gc = len([x for x in c if x in gemelos_list])
    if usar_gem and gc != 1: return False
    if not usar_gem and gc > 0: return False
    
    # 6. CONSECUTIUS
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    if usar_cons and cc != 1: return False
    if not usar_cons and cc > 0: return False
    
    # 7. TERMINACIONS (Màx 2 iguals)
    if f_term:
        terms = [x % 10 for x in c]
        if any(terms.count(i) > 2 for i in range(10)): return False
    
    # Solapament màxim entre combinacions
    for ant in anteriores:
        if len(set(c) & set(ant)) > 2: return False
        
    return True

# --- UI ---
st.title("PRIMITIVA PRO v15")
st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>9.500.000 €</div>', unsafe_allow_html=True)

# Resultats anteriors
for s in sorteigs_reals:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card"><strong>📅 {s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div></div>', unsafe_allow_html=True)

st.divider()

# Panell de control
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Decenes (Patró 2-2-1-1-1)", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alternança Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Alternança Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (3 primeres)", value=True)
cons_on = st.toggle("Filtre: Consecutius (3 primeres)", value=True)
f_term = st.toggle("Filtre: Terminacions", value=True)

# Generador
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚMEROS)"):
    finales = []
    rs_top = [2, 5, 8, 0, 3, 9]
    intents = 0
    while len(finales) < 6 and intents < 100000:
        t_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        t_ps = "4P3S" if len(finales) % 3 == 0 else "3P4S"
        u_gem = gem_on if len(finales) < 3 else False
        u_cons = cons_on if len(finales) < 3 else False
        
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 7 and validar_estricte_v15(c, finales, f_dec, f_suma, f_ab, f_ps, f_term, u_gem, u_cons, t_ab, t_ps):
            finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("⚠️ Filtres molt estrictes. L'algoritme 2-2-1-1-1 necessita més intents o desactivar algun filtre.")
    else:
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)

st.info("S'ha restaurat el filtre de desenes 2-2-1-1-1: garanteix que els 7 números estiguin repartits en totes les franges de desenes.")
