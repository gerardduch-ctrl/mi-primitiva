import streamlit as st
import random

# --- 1. CONFIGURACIÓ I ESTIL ---
st.set_page_config(page_title="Primitiva Pro v34", page_icon="P", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    /* Selectors visibles en mòbil */
    div[data-testid="stWidgetLabel"] p, label p {
        color: black !important; font-weight: 900 !important; font-size: 16px !important; opacity: 1 !important;
    }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; text-align: left; line-height: 1.5; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stats-box { background-color: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; margin: 15px 0; font-weight: bold; color: #856404; text-align: center; font-size: 12px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADES REALS I CONSTANTS ---
SORTEIGS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

GEMELOS = {11, 22, 33, 44}

# --- 3. MOTOR DE VALIDACIÓ ---
def validar_completo(c, anteriores, f_dec, f_suma, f_ab, f_ps, f_term, usar_gem, usar_cons, t_ab, t_ps):
    is_7 = len(c) == 7
    # Decenes 2-2-1-1-1 (o 2-1-1-1-1 per a 6 números)
    decs = [(x-1)//10 for x in c]
    target = [2, 2, 1, 1, 1] if is_7 else [2, 1, 1, 1, 1]
    if f_dec and sorted([decs.count(i) for i in range(5)], reverse=True) != target: return False
    
    # Suma
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    if f_suma and not (l_inf <= s_tot <= l_sup): return False
    
    # Alts/Baixos i Parells/Senars
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    if f_ab and bajos != (4 if t_ab == "4B3A" else 3): return False
    if f_ps and pares != (4 if t_ps == "4P3S" else 3): return False
    
    # Bessons
    gc = len([x for x in c if x in GEMELOS])
    if (usar_gem and gc != 1) or (not usar_gem and gc > 0): return False
    
    # Consecutius
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    if (usar_cons and cc != 1) or (not usar_cons and cc > 0): return False
    
    # Terminacions
    if f_term:
        terms = [x % 10 for x in c]
        if any(terms.count(i) > 2 for i in range(10)): return False
        
    # Solapament
    if any(len(set(c) & set(ant)) > 2 for ant in anteriores): return False
    
    return True

# --- UI: BOTE I HISTÒRIC ---
st.markdown('<div class="bote-box">BOTE ACTUAL:<br>9.500.000 €</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Històric Detallat")
for s in SORTEIGS:
    c = s['nums']
    decs = [(x-1)//10 for x in c]
    s_tot = sum(c)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in GEMELOS])
    sc = sorted(c)
    cc = sum(1 for i in range(5) if sc[i+1]-sc[i] == 1)
    n_html = "".join([f'<div class="num">{x}</div>' for x in c])
    
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">
                {'✅' if sorted([decs.count(i) for i in range(5)], reverse=True) == [2,1,1,1,1] else '❌'} Decenes | 
                {'✅' if 131 <= s_tot <= 160 else '❌'} Suma ({s_tot}) | 
                {'✅' if bajos in [3,4] else '❌'} A/B ({bajos}B) | 
                {'✅' if pares in [3,4] else '❌'} P/S ({pares}P) | 
                {'✅' if gc == 1 else '❌'} Bessons | 
                {'✅' if cc == 1 else '❌'} Cons | 
                Term: {'✅' if all([x%10 for x in c].count(i)<=2 for i in range(10)) else '❌'}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- UI: PANELL DE CONTROL ---
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Suma (150-220)", value=True)
f_ab = st.toggle("Alternança Alts/Baixos", value=True)
f_ps = st.toggle("Alternança Parells/Senars", value=True)
gem_on = st.toggle("Bessons (3 primeres)", value=True)
cons_on = st.toggle("Consecutius (1, 3, 5)", value=True)
f_term = st.toggle("Terminacions (Màx 2)", value=True)

# CÀLCUL DE PROBABILITAT
total = 13983816
rest = total
if f_dec: rest *= 0.18
if f_suma: rest *= 0.15
if f_ab: rest *= 0.35
if f_ps: rest *= 0.35
if gem_on: rest *= 0.12
if cons_on: rest *= 0.40
st.markdown(f'<div class="stats-box">Total: {total:,} | Criteris: {int(rest):,} combinacions simples</div>', unsafe_allow_html=True)

# --- GENERADOR ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    rs_gen = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        
        c = sorted(random.sample(range(1, 50), 7))
        if validar_completo(c, finales, f_dec, f_suma, f_ab, f_ps, f_term, u_gem, u_cons, t_ab, t_ps):
            finales.append(c)
        intents += 1

    if finales:
        for i, f in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in f])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs_gen[i]}</div></div>', unsafe_allow_html=True)
    else:
        st.warning("Massa filtres. Prova de nou.")
