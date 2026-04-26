import streamlit as st
import random
from itertools import combinations

# --- CONFIGURACIÓ I ESTIL ---
st.set_page_config(page_title="P - Primitiva Pro", page_icon="P")

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

# --- DADES REALS I GRUPS ---
SORTEIGS_REALS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

CALIENTES = [3, 23, 30, 38, 39, 47, 49, 1, 2, 45]
DESPERTANDO = [x for x in range(1, 50) if x not in CALIENTES][:20]
HIELO = [x for x in range(1, 50) if x not in CALIENTES and x not in DESPERTANDO][:15]
GEMELOS = {11, 22, 33, 44}

# --- DIAGNÒSTIC TOTAL (Tots els paràmetres) ---
def analitzar_total(c):
    is_7 = len(c) == 7
    decs = [(x-1)//10 for x in c]
    counts = [decs.count(i) for i in range(5)]
    ok_dec = all(cnt > 0 for cnt in counts) and all(cnt <= 2 for cnt in counts) if is_7 else all(cnt <= 2 for cnt in counts)
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in GEMELOS])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    t = [x % 10 for x in c]
    ok_t = all(t.count(i) <= 2 for i in range(10))
    return [
        f"{'✅' if ok_dec else '❌'} Dec", f"{'✅' if l_inf <= s_tot <= l_sup else '❌'} Sum({s_tot})",
        f"{'✅' if bajos==4 else '❌'} A/B({bajos}B)", f"{'✅' if (pares==3 or pares==4) else '❌'} P/S({pares}P)",
        f"{'✅' if gc==1 else '❌'} Bes", f"{'✅' if cc==1 else '❌'} Cons", f"{'✅' if ok_t else '❌'} Term"
    ]

# --- UI: BOTE I HISTÒRIC ---
st.markdown('<div class="bote-box">BOTE ACTUAL:<br>9.500.000 €</div>', unsafe_allow_html=True)
for s in SORTEIGS_REALS:
    checks = analitzar_total(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card"><strong>📅 {s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div><div class="diag-box">{" | ".join(checks)}</div></div>', unsafe_allow_html=True)

st.divider()

# --- PANELL DE CONTROL ---
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)

# --- GENERADOR AMB REINTEGRE ORIGINAL ---
if st.button("GENERAR APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    # Lògica Reintegres Original (3 baixos, 3 alts segons versió d'origen)
    rs_orig = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        c = sorted(random.sample(CALIENTES, 1) + random.sample(DESPERTANDO, 4) + random.sample(HIELO, 2))
        
        if len(set(c)) == 7:
            decs = [(x-1)//10 for x in c]
            if f_dec and (any(decs.count(i)==0 for i in range(5)) or any(decs.count(i)>2 for i in range(5))): continue
            if f_suma and not (150 <= sum(c) <= 220): continue
            gc = len([x for x in c if x in GEMELOS])
            if (u_gem and gc != 1) or (not u_gem and gc > 0): continue
            cc = sum(1 for i in range(6) if c[i+1]-c[i] == 1)
            if (u_cons and cc != 1) or (not u_cons and cc > 0): continue
            if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
            finales.append(c)
        intents += 1

    if finales:
        for i, f in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in f])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs_orig[i]}</div></div>', unsafe_allow_html=True)
