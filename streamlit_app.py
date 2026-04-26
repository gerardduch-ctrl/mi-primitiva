import streamlit as st
import random
from itertools import combinations

# --- 1. CONFIGURACIÓ I ESTIL ---
st.set_page_config(page_title="P - Primitiva Pro v25", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; text-align: left; line-height: 1.5; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADES REALS I HISTORIAL DE SEGURETAT ---
SORTEIGS_REALS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

# Historial resumit per a la comprovació inèdita (Frozensets per ràpida cerca)
HISTORIAL_GUANYADORS = {frozenset(s['nums']) for s in SORTEIGS_REALS} | {frozenset([1,2,3,4,5,6])} 

# --- 3. GRUPS PER TEMPERATURA ---
N = list(range(1, 50))
CALIENTES = [3, 23, 30, 38, 39, 47, 45, 1, 15, 2] # 10 núm
DESPERTANDO = [x for x in N if x not in CALIENTES][:20] # 20 núm
HIELO = [x for x in N if x not in CALIENTES and x not in DESPERTANDO][:15] # 15 núm
GEMELOS = {11, 22, 33, 44}

# --- 4. MOTOR DE VALIDACIÓ ---
def validar_v25(c, anteriores, f_dec, f_suma, f_ab, f_ps, f_term, usar_gem, usar_cons):
    # Decenes: Totes les desenes presents, màxim 2 per desena (2-2-1-1-1)
    decs = [(x-1)//10 for x in c]
    counts = [decs.count(i) for i in range(5)]
    if f_dec:
        if any(cnt == 0 for cnt in counts) or any(cnt > 2 for cnt in counts): return False
    
    # Suma: 131-160
    if f_suma and not (131 <= sum(c) <= 160): return False
    
    # Alts/Baixos: 4 Baixos (1-25) i 3 Alts (26-49)
    bajos = len([x for x in c if x <= 25])
    if f_ab and bajos != 4: return False
    
    # Bessons: Exactament 1 (si toca) o 0
    gc = len([x for x in c if x in GEMELOS])
    if (usar_gem and gc != 1) or (not usar_gem and gc > 0): return False
    
    # Consecutius: Exactament 1 parella (si toca) o 0
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    if (usar_cons and cc != 1) or (not usar_cons and cc > 0): return False

    # Solapament: Màx 2 números amb anteriors generades
    if any(len(set(c) & set(ant)) > 2 for ant in anteriores): return False
    
    # Inèdita: No pot haver estat guanyadora de 6
    for sub in combinations(c, 6):
        if frozenset(sub) in HISTORIAL_GUANYADORS: return False

    return True

# --- 5. UI: BOTE I HISTÒRIC ---
st.markdown('<div class="bote-box">BOTE ACTUAL:<br>9.500.000 €</div>', unsafe_allow_html=True)

for s in SORTEIGS_REALS:
    c = s['nums']
    decs = [(x-1)//10 for x in c]
    s_tot = sum(c)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in GEMELOS])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    
    n_html = "".join([f'<div class="num">{x}</div>' for x in c])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">
                {'✅' if all(decs.count(i)>0 for i in range(5)) else '❌'} Dec | 
                {'✅' if 131<=s_tot<=160 else '❌'} Suma ({s_tot}) | 
                {'✅' if bajos==4 else '❌'} A/B ({bajos}B) | 
                {'✅' if pares in [3,4] else '❌'} P/S | 
                {'✅' if gc==1 else '❌'} Bes | 
                {'✅' if cc==1 else '❌'} Cons
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 6. PANELL DE CONTROL ---
st.subheader("⚙️ Filtres")
f_dec = st.toggle("Filtre: Decenes (2-2-1-1-1)", value=True)
f_suma = st.toggle("Filtre: Suma (131-160)", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos (4B/3A)", value=True)
f_ps = st.toggle("Filtre: Parells/Senars (3P/4S o 4P/3S)", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)

# --- 7. GENERADOR ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    rs_gen = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        # Regla Parells/Senars: 3 primeres (3P/4S), 3 últimes (4P/3S)
        t_ps = "3P4S" if idx < 3 else "4P3S"
        # Regles Bessons i Consecutius específiques
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        
        # Selecció per temperatura: 1 Cal + 4 Desp + 2 Hielo
        c = sorted(random.sample(CALIENTES, 1) + random.sample(DESPERTANDO, 4) + random.sample(HIELO, 2))
        
        # Validació Parells/Senars extra
        pares = len([x for x in c if x % 2 == 0])
        ok_ps = (pares == (3 if t_ps == "3P4S" else 4)) if f_ps else True
        
        if ok_ps and validar_v25(c, finales, f_dec, f_suma, f_ab, f_ps, True, u_gem, u_cons):
            finales.append(c)
        intents += 1

    if finales:
        for i, f in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in f])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs_gen[i]}</div></div>', unsafe_allow_html=True)
