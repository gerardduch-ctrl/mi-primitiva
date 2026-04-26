import streamlit as st
import random
from datetime import datetime

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva", page_icon="P")

# CSS per forçar NEGRETA, COLOR NEGRE i minimalisme total (EL TEU ORIGINAL)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 15px; border: 2px solid black; margin-bottom: 12px; text-align: center; background-color: #fff; }
    .num { display: inline-block; width: 32px; height: 32px; line-height: 32px; border-radius: 50%; border: 2px solid black; margin: 3px; font-weight: bold; font-size: 14px; color: black; }
    .r-num { background-color: black; color: white; }
    .stButton>button { background-color: black !important; color: white !important; border: none; width: 100%; height: 55px; font-weight: bold; border-radius: 0px; font-size: 18px; }
    .tit-selector { font-size: 18px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid black; display: inline-block; width: 100%; color: black; text-transform: uppercase; }
    div[data-testid="stRadio"] label p { font-size: 20px !important; font-weight: 900 !important; color: black !important; opacity: 1 !important; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f9f9f9; border-radius: 3px; font-size: 11px; text-align: left; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    div[data-testid="stVerticalBlock"] > div:has(div.tit-selector) { padding-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# DADES AFEGIDES (Resultats reals i Bote)
SORTEIGS_REALS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Lunes 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

# Lògica interna (EL TEU ORIGINAL)
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
    # 5. Solapament Máx 2 números
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

def analitzar_total(c):
    d = [(x-1)//10 for x in c]
    s_tot = sum(c)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in gemelos_list])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    t = [x % 10 for x in c]
    ok_t = all(t.count(i) <= 2 for i in range(10))
    return [
        f"{'✅' if (all(d.count(i)>0 for i in range(5)) and all(d.count(i)<=2 for i in range(5))) else '❌'} Dec",
        f"{'✅' if 131<=s_tot<=160 else '❌'} Sum({s_tot})",
        f"{'✅' if bajos==4 else '❌'} A/B({bajos}B)",
        f"{'✅' if pares in [3,4] else '❌'} P/S({pares}P)",
        f"{'✅' if gc==1 else '❌'} Bes",
        f"{'✅' if cc==1 else '❌'} Cons",
        f"{'✅' if ok_t else '❌'} Term"
    ]

# --- INTERFÍCIE ---
st.title("PRIMITIVA v1 PRO")

# BOTE (Dada real)
st.markdown('<div class="bote-box">PROPER SORTEIG BOTE:<br>9.500.000 €</div>', unsafe_allow_html=True)

# ÚLTIMS RESULTATS AMB DIAGNÒSTIC
st.subheader("Anàlisi Històric Detallat")
for s in SORTEIGS_REALS:
    checks = analitzar_total(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(checks)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# SELECTORS (EL TEU ORIGINAL)
st.markdown('<p class="tit-selector">NÚMEROS BESSONS</p>', unsafe_allow_html=True)
gem_on = st.radio("Gemelos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

st.markdown('<p class="tit-selector">NÚMEROS CONSECUTIUS</p>', unsafe_allow_html=True)
cons_on = st.radio("Consecutivos", ["OFF", "ON"], label_visibility="collapsed", horizontal=True) == "ON"

if st.button("GENERAR COMBINACIONS"):
    finales = []
    rs = random.sample(range(10), 6) # (EL TEU ORIGINAL)
    
    intentos = 0
    while len(finales) < 6 and intentos < 35000:
        tipo = "3P4I" if len(finales) < 3 else "4P3I"
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
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
