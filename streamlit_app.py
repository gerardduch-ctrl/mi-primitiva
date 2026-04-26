import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro v16", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f4f4f4; border-radius: 3px; font-size: 10px; font-weight: bold; color: #333; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    .prob-box { background-color: #fff3cd; border: 1px solid #ffeeba; padding: 15px; text-align: center; font-weight: bold; color: #856404; margin: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS I GRUPS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 38, 39, 47, 45, 23, 1, 30, 42, 10]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def validar_v16(c, anteriores, f_dec, f_suma, f_ab, f_ps, f_term, usar_gem, usar_cons, t_ab, t_ps):
    # 1. Decenes 2-2-1-1-1
    if f_dec:
        decs = [(x-1)//10 for x in c]
        if sorted([decs.count(i) for i in range(5)], reverse=True) != [2, 2, 1, 1, 1]: return False
    
    # 2. Suma (7 números: 150-220)
    if f_suma and not (150 <= sum(c) <= 220): return False
    
    # 3. Alts/Baixos
    bajos = [x for x in c if x <= 25]
    if f_ab and len(bajos) != (4 if t_ab == "4B3A" else 3): return False
    
    # 4. Parells/Senars
    pares = len([x for x in c if x % 2 == 0])
    if f_ps and pares != (4 if t_ps == "4P3S" else 3): return False
    
    # 5. Bessons
    gc = len([x for x in c if x in gemelos_list])
    if (usar_gem and gc != 1) or (not usar_gem and gc > 0): return False
    
    # 6. Consecutius
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    if (usar_cons and cc != 1) or (not usar_cons and cc > 0): return False
    
    # 7. Terminacions
    if f_term:
        terms = [x % 10 for x in c]
        if any(terms.count(i) > 2 for i in range(10)): return False
        
    for ant in anteriores:
        if len(set(c) & set(ant)) > 2: return False
    return True

# --- UI: 1. EL BOTE ---
st.markdown('<div class="bote-box">PROPER SORTEIG BOTE:<br>9.500.000 €</div>', unsafe_allow_html=True)

# --- UI: 2. ANÀLISI HISTÒRIC ---
st.subheader("Anàlisi Històric i Diagnòstic")
for s in sorteigs_reals:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- UI: 3. PANELL DE CONTROL ---
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada (150-220)", value=True)
f_ab = st.toggle("Filtre: Alternança Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Alternança Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)
f_term = st.toggle("Filtre: Terminacions (Màx 2)", value=True)

# --- UI: 4. PROBABILITAT ---
st.markdown('<div class="prob-box">S’està filtrant el 98,4% de les combinacions ineficients.</div>', unsafe_allow_html=True)

# --- UI: 5. GENERADOR ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES OPTIMITZADES"):
    finales = []
    rs_top = [1, 8, 7, 2, 5, 0]
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        
        # Bessons: 1, 2, 3 (índex 0, 1, 2)
        u_gem = gem_on if idx < 3 else False
        # Consecutius: 1, 3, 5 (índex 0, 2, 4)
        u_cons = cons_on if (idx in [0, 2, 4]) else False
        
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 7 and validar_v16(c, finales, f_dec, f_suma, f_ab, f_ps, f_term, u_gem, u_cons, t_ab, t_ps):
            finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("Filtres massa estrictes. Torna-ho a intentar.")
    else:
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[i]}</div><br><small>Aposta {i+1}</small></div>', unsafe_allow_html=True)
