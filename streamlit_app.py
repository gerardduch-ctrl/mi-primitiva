import streamlit as st
import random
import time
from itertools import combinations

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Pro Final", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; text-align: left; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS I GRUPS ---
@st.cache_data(ttl=3600)
def dades_fix_reals():
    return [
        {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ], "9.500.000 €"

sorteigs, bote = dades_fix_reals()
gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 23, 30, 38, 39, 45, 47]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

# --- LÒGICA DE DIAGNÒSTIC (Tots els paràmetres) ---
def analitzar_total(c):
    is_7 = len(c) == 7
    d = [(x-1)//10 for x in c]
    counts = sorted([d.count(i) for i in range(5)], reverse=True)
    target = [2, 2, 1, 1, 1] if is_7 else [2, 1, 1, 1, 1]
    
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in gemelos_list])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    t = [x % 10 for x in c]
    ok_t = all(t.count(i) <= 2 for i in range(10))

    return [
        f"{'✅' if counts == target else '❌'} Decenes",
        f"{'✅' if l_inf <= s_tot <= l_sup else '❌'} Suma ({s_tot})",
        f"{'✅' if bajos in [3, 4] else '❌'} A/B ({bajos}B)",
        f"{'✅' if pares in [3, 4] else '❌'} P/S ({pares}P)",
        f"{'✅' if gc == 1 else '❌'} Bessons",
        f"{'✅' if cc == 1 else '❌'} Consecutius",
        f"{'✅' if ok_t else '❌'} Terminacions"
    ]

# --- UI: BOTE I HISTÒRIC ---
st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote}</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Històric Reial")
for s in sorteigs:
    checks = analitzar_total(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(checks)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- UI: PANELL DE CONTROL ---
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (1-3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (1-3-5)", value=True)
f_term = st.toggle("Filtre: Terminacions", value=True)

# --- GENERADOR AMB REINTEGRE ORIGINAL ---
if st.button("GENERAR APOSTES OPTIMITZADES"):
    finales = []
    # Lògica original: Reintegres (3 Frios, 3 Despertando)
    reintegres = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    
    with st.status("🚀 Generant combinacions inèdites...", expanded=False):
        intents = 0
        while len(finales) < 6 and intents < 100000:
            idx = len(finales)
            t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
            t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
            u_gem = gem_on if idx < 3 else False
            u_cons = cons_on if idx in [0, 2, 4] else False
            
            c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
            
            if len(set(c)) == 7:
                # Comprovació solapament i estadístiques
                if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
                
                decs = [(x-1)//10 for x in c]
                if f_dec and sorted([decs.count(i) for i in range(5)], reverse=True) != [2, 2, 1, 1, 1]: continue
                if f_suma and not (150 <= sum(c) <= 220): continue
                
                bajos = len([x for x in c if x <= 25])
                if f_ab and bajos != (4 if t_ab == "4B3A" else 3): continue
                
                gc = len([x for x in c if x in gemelos_list])
                if (u_gem and gc != 1) or (not u_gem and gc > 0): continue
                
                cc = sum(1 for i in range(6) if c[i+1]-c[i] == 1)
                if (u_cons and cc != 1) or (not u_cons and cc > 0): continue
                
                finales.append(c)
            intents += 1

    if finales:
        st.subheader("Les teves Apostes de 7 Números")
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{reintegres[i]}</div></div>', unsafe_allow_html=True)
