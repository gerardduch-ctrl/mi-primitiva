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
    .diag-box { margin-top: 8px; padding: 5px; background: #f4f4f4; border-radius: 3px; font-size: 11px; font-weight: bold; color: #d32f2f; }
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
cal_hist = [38, 39, 47, 3, 45, 30, 42, 11, 22, 7]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def analitzar_puntos(c, f_dec, f_suma, f_ab, f_ps, f_gem, f_cons, f_term, is_7=False):
    puntos = 0
    # 1. Decenes 2-2-1-1-1 (o 2-1-1-1-1 per 6 nums)
    decs = [(x-1)//10 for x in c]
    counts = sorted([decs.count(i) for i in range(5)], reverse=True)
    target = [2, 2, 1, 1, 1] if len(c) == 7 else [2, 1, 1, 1, 1]
    if counts == target: puntos += 1
    
    # 2. Suma
    s_total = sum(c)
    lim_inf, lim_sup = (150, 220) if len(c) == 7 else (131, 160)
    if lim_inf <= s_total <= lim_sup: puntos += 1
    
    # 3. Alts/Baixos (Equilibri)
    bajos = [x for x in c if x <= 25]
    if len(bajos) in [3, 4]: puntos += 1
    
    # 4. Parells/Senars (Equilibri)
    pares = len([x for x in c if x % 2 == 0])
    if pares in [3, 4]: puntos += 1
    
    # 5. Bessons
    gc = len([x for x in c if x in gemelos_list])
    if gc == 1: puntos += 1
    
    # 6. Consecutius
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    if cc == 1: puntos += 1
    
    # 7. Terminacions (Màx 2)
    terms = [x % 10 for x in c]
    if all(terms.count(i) <= 2 for i in range(10)): puntos += 1
    
    return puntos

# --- UI: EL BOTE ---
st.markdown('<div class="bote-box">PROPER SORTEIG BOTE:<br>9.500.000 €</div>', unsafe_allow_html=True)

# --- UI: ANÀLISI HISTÒRIC ---
st.subheader("Anàlisi Històric (6 números)")
for s in sorteigs_reals:
    pts = analitzar_puntos(s['nums'], True, True, True, True, True, True, True)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">Aquesta combinació respecta {pts} de 7 paràmetres analitzats</div>
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
        
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 7:
            # Validació interna segons els toggles
            decs = [(x-1)//10 for x in c]
            cond_dec = (sorted([decs.count(i) for i in range(5)], reverse=True) == [2, 2, 1, 1, 1]) if f_dec else True
            cond_sum = (150 <= sum(c) <= 220) if f_suma else True
            bajos = [x for x in c if x <= 25]
            cond_ab = (len(bajos) == (4 if t_ab == "4B3A" else 3)) if f_ab else True
            pares = len([x for x in c if x % 2 == 0])
            cond_ps = (pares == (4 if t_ps == "4P3S" else 3)) if f_ps else True
            gc = len([x for x in c if x in gemelos_list])
            cond_gem = (gc == 1) if u_gem else (gc == 0)
            sc = sorted(c)
            cc = sum(1 for i in range(6) if sc[i+1]-sc[i] == 1)
            cond_cons = (cc == 1) if u_cons else (cc == 0)
            terms = [x % 10 for x in c]
            cond_term = all(terms.count(i) <= 2 for i in range(10)) if f_term else True
            
            if all([cond_dec, cond_sum, cond_ab, cond_ps, cond_gem, cond_cons, cond_term]):
                finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("Filtres massa estrictes. Prova de nou.")
    else:
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[i]}</div><br><small>Aposta {i+1} (7 números)</small></div>', unsafe_allow_html=True)
