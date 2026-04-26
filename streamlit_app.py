import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro v18", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 11px; text-align: left; line-height: 1.5; color: #333; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS I GRUPS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

gemelos_list = [11, 22, 33, 44]
cal_hist = [38, 39, 47, 3, 45, 1, 40, 2, 11, 30]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def diagnostic_detallat(c):
    is_7 = len(c) == 7
    checks = []
    decs = [(x-1)//10 for x in c]
    counts = sorted([decs.count(i) for i in range(5)], reverse=True)
    target = [2, 2, 1, 1, 1] if is_7 else [2, 1, 1, 1, 1]
    checks.append(f"{'✅' if counts == target else '❌'} Decenes ({'-'.join(map(str, counts))})")
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    checks.append(f"{'✅' if l_inf <= s_tot <= l_sup else '❌'} Suma ({s_tot})")
    bajos = len([x for x in c if x <= 25])
    checks.append(f"{'✅' if bajos in [3, 4] else '❌'} Alts/Baixos ({bajos}B)")
    pares = len([x for x in c if x % 2 == 0])
    checks.append(f"{'✅' if pares in [3, 4] else '❌'} Parells/Senars ({pares}P)")
    gc = len([x for x in c if x in gemelos_list])
    checks.append(f"{'✅' if gc == 1 else '❌'} Bessons ({gc})")
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    checks.append(f"{'✅' if cc == 1 else '❌'} Consecutius ({cc})")
    terms = [x % 10 for x in c]
    checks.append(f"{'✅' if all(terms.count(i) <= 2 for i in range(10)) else '❌'} Terminacions (Màx 2)")
    return checks

# --- UI: EL BOTE ---
st.markdown('<div class="bote-box">PROPER SORTEIG BOTE:<br>9.500.000 €</div>', unsafe_allow_html=True)

# --- UI: ANÀLISI HISTÒRIC ---
st.subheader("Anàlisi Històric Detallat")
for s in sorteigs_reals:
    checks = diagnostic_detallat(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{"<br>".join(checks)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- UI: PANELL DE CONTROL ---
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada (150-220)", value=True)
f_ab = st.toggle("Filtre: Alternança Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Alternança Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)
f_term = st.toggle("Filtre: Terminacions (Màx 2)", value=True)

# --- UI: GENERADOR ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚMEROS)"):
    finales = []
    rs_top = [random.randint(0,9) for _ in range(6)]
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        
        c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
        
        if len(set(c)) == 7:
            # 1. FILTRE DE SOLAPAMENT (MÀX 2 NÚMEROS IGUALS AMB LES ANTERIORS)
            if any(len(set(c) & set(ant)) > 2 for ant in finales):
                intents += 1
                continue
                
            decs = [(x-1)//10 for x in c]
            cond_dec = (sorted([decs.count(i) for i in range(5)], reverse=True) == [2, 2, 1, 1, 1]) if f_dec else True
            cond_sum = (150 <= sum(c) <= 220) if f_suma else True
            bajos = len([x for x in c if x <= 25])
            cond_ab = (bajos == (4 if t_ab == "4B3A" else 3)) if f_ab else True
            pares = len([x for x in c if x % 2 == 0])
            cond_ps = (pares == (4 if t_ps == "4P3S" else 3)) if f_ps else True
            gc = len([x for x in c if x in gemelos_list])
            cond_gem = (gc == 1) if u_gem else (gc == 0)
            cc = sum(1 for i in range(6) if c[i+1]-c[i] == 1)
            cond_cons = (cc == 1) if u_cons else (cc == 0)
            terms = [x % 10 for x in c]
            cond_term = all(terms.count(i) <= 2 for i in range(10)) if f_term else True
            
            if all([cond_dec, cond_sum, cond_ab, cond_ps, cond_gem, cond_cons, cond_term]):
                finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("⚠️ Filtres massa exigents per al solapament. Prova de nou.")
    else:
        st.subheader("Les teves Apostes de 7 Números")
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[i]}</div><br><small>Aposta {i+1} (Màx 2 coincidències)</small></div>', unsafe_allow_html=True)
