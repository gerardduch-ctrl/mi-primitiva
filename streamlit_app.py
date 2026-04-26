import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro", page_icon="P")

# CSS per forçar NEGRETA, COLOR NEGRE i minimalisme total
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 12px; text-align: center; background-color: #fff; }
    .num { display: inline-block; width: 30px; height: 30px; line-height: 30px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; color: black; text-align: center; }
    .r-num { background-color: black; color: white; }
    .stButton>button { background-color: black !important; color: white !important; border: none; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; }
    .tit-selector { font-size: 18px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid black; display: inline-block; width: 100%; color: black; text-transform: uppercase; }
    div[data-testid="stRadio"] label p { font-size: 20px !important; font-weight: 900 !important; color: black !important; opacity: 1 !important; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f9f9f9; border-radius: 3px; font-size: 11px; text-align: left; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS I CONSTANTS ---
SORTEIGS_REALS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]
BOTE_ACTUAL = "9.500.000 €"

n = list(range(1, 50))
desp = random.sample(n, 20)
hielo = random.sample(n, 15)
cal = random.sample(n, 10)
gemelos_list = [11, 22, 33, 44]

# --- LÒGICA DE VALIDACIÓ ---
def validar_final(combo, anteriores, con_gem, con_cons, tipo):
    # 1. Decenes 2-2-1-1-1
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
    # 5. Solapament Màx 2
    for ant in anteriores:
        if len(set(combo) & set(ant)) > 2: return False
    # 6. Gemelos
    g_count = len([x for x in combo if x in gemelos_list])
    if con_gem and g_count != 1: return False
    if not con_gem and g_count > 0: return False
    # 7. Consecutius
    s = sorted(combo)
    c_count = sum(1 for i in range(len(s)-1) if s[i+1]-s[i] == 1)
    if con_cons and c_count != 1: return False
    if not con_cons and c_count > 0: return False
    return True

def analitzar_total(c):
    # Diagnòstic adaptat per a 6 o 7 números
    is_7 = len(c) == 7
    d = [(x-1)//10 for x in c]
    s_tot = sum(c)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in gemelos_list])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    
    # Regles del diagnòstic
    target_dec = all(d.count(i) > 0 for i in range(5))
    target_sum = 131 <= s_tot <= 160
    target_ab = bajos == 4
    target_ps = pares in [3, 4]
    target_bes = gc == 1
    target_cons = cc == 1
    target_term = all([ (x%10) for x in c].count(i) <= 2 for i in range(10))

    return [
        f"{'✅' if target_dec else '❌'} Dec", f"{'✅' if target_sum else '❌'} Suma({s_tot})",
        f"{'✅' if target_ab else '❌'} A/B({bajos}B)", f"{'✅' if target_ps else '❌'} P/S({pares}P)",
        f"{'✅' if target_bes else '❌'} Bes", f"{'✅' if target_cons else '❌'} Cons",
        f"{'✅' if target_term else '❌'} Term"
    ]

# --- INTERFÍCIE ---
st.title("PRIMITIVA v1 PRO")

# 1. EL BOTE
st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{BOTE_ACTUAL}</div>', unsafe_allow_html=True)

# 2. ÚLTIMS RESULTATS AMB DIAGNÒSTIC
st.subheader("Anàlisi Històric Detallat")
for s in SORTEIGS_REALS:
    checks = analitzar_total(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <div style="font-size:16px; margin-bottom:8px;">📅 <strong>{s['data']}</strong></div>
            {n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(checks)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# 3. SELECTORS (Originals restaurats)
st.markdown('<p class="tit-selector">NÚMEROS BESSONS</p>', unsafe_allow_html=True)
gem_on = st.radio("Gemelos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

st.markdown('<p class="tit-selector">NÚMEROS CONSECUTIUS</p>', unsafe_allow_html=True)
cons_on = st.radio("Consecutivos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

# 4. GENERADOR (Lògica original de 7 números i 6 apostes)
if st.button("GENERAR COMBINACIONS"):
    finales = []
    # Reintegres aleatoris 0-9
    rs = random.sample(range(10), 6)
    
    intentos = 0
    while len(finales) < 6 and intentos < 50000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        # Generació base 4 Desp + 2 Hielo + 1 Cal (7 números)
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

st.write(f"Data generació: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
