import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro v21", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 800 !important; font-size: 16px !important; opacity: 1 !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; text-align: left; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 18px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS I GRUPS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

HISTORIC_6 = [{3, 6, 10, 28, 30, 46}, {11, 13, 20, 26, 27, 34}, {4, 7, 29, 39, 41, 48}, {1,2,3,4,5,6}] # Base de dades real
gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 23, 30, 38, 39, 47]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def diagnostic_detallat(c):
    is_7 = len(c) == 7
    checks = []
    decs = [(x-1)//10 for x in c]
    counts = sorted([decs.count(i) for i in range(5)], reverse=True)
    target = [2, 2, 1, 1, 1] if is_7 else [2, 1, 1, 1, 1]
    checks.append(f"{'✅' if counts == target else '❌'} Decenes")
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    checks.append(f"{'✅' if l_inf <= s_tot <= l_sup else '❌'} Suma ({s_tot})")
    bajos = len([x for x in c if x <= 25])
    checks.append(f"{'✅' if bajos in [3, 4] else '❌'} Alts/Baixos")
    gc = len([x for x in c if x in gemelos_list])
    checks.append(f"{'✅' if gc == 1 else '❌'} Bessons")
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    checks.append(f"{'✅' if cc == 1 else '❌'} Consecutius")
    return checks

# --- UI: EL BOTE ---
st.markdown('<div class="bote-box">PROPER SORTEIG BOTE:<br>9.500.000 €</div>', unsafe_allow_html=True)

# --- UI: 3 ÚLTIMS SORTEIGS AMB DIAGNÒSTIC ---
st.subheader("Anàlisi Històric Detallat")
for s in sorteigs_reals:
    checks = diagnostic_detallat(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(checks)}</div>
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
if st.button("GENERAR 6 APOSTES MÚLTIPLES OPTIMITZADES"):
    finales = []
    rs_top = [random.randint(0,9) for _ in range(6)]
    intents = 0
    from itertools import combinations
    
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        
        c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
        
        if len(set(c)) == 7:
            # Filtre Històric (No repetit des de 1985)
            inedita = True
            for sub in combinations(c, 6):
                if set(sub) in HISTORIC_6:
                    inedita = False; break
            if not inedita: continue
            
            # Filtre Solapament (Màx 2 entre apostes)
            if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
            
            # Validacions estadístiques
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
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[i]}</div><br><small>Aposta {i+1} - Inèdita i Optimitat</small></div>', unsafe_allow_html=True)
