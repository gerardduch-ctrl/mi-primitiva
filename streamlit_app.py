import streamlit as st
import random

# --- 1. CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro v31", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 14px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; line-height: 1.5; color: #333; font-weight: bold; text-align: left; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stats-box { background-color: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; margin: 15px 0; font-family: monospace; font-size: 12px; color: #856404; text-align: center; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADES REALS I GRUPS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 23, 30, 38, 39, 47]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

# --- 3. FUNCIÓ DE DIAGNÒSTIC ---
def analitzar_v31(c):
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
    terms = [x % 10 for x in c]
    ok_t = all(terms.count(i) <= 2 for i in range(10))

    return {
        "Dec": counts == target, "Sum": l_inf <= s_tot <= l_sup,
        "AB": bajos in [3, 4], "PS": pares in [3, 4],
        "Bes": gc == 1, "Cons": cc == 1, "Term": ok_t,
        "val_sum": s_tot, "val_ab": f"{bajos}B", "val_ps": f"{pares}P"
    }

# --- UI: BOTE I HISTÒRIC ---
st.markdown(f'<div class="bote-box">BOTE PROPER SORTEIG:<br>9.500.000 €</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Històric Detallat")
for s in sorteigs_reals:
    res = analitzar_v31(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">
                {'✅' if res['Dec'] else '❌'} Decenes | {'✅' if res['Sum'] else '❌'} Suma ({res['val_sum']}) | 
                {'✅' if res['AB'] else '❌'} A/B ({res['val_ab']}) | {'✅' if res['PS'] else '❌'} P/S ({res['val_ps']}) |
                {'✅' if res['Bes'] else '❌'} Bessons | {'✅' if res['Cons'] else '❌'} Cons | 
                {'✅' if res['Term'] else '❌'} Terminacions
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- UI: PANELL DE CONTROL ---
st.subheader("⚙️ Configuració i Probabilitat")
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (3 primeres)", value=True)
cons_on = st.toggle("Filtre: Consecutius (1, 3, 5)", value=True)
f_term = st.toggle("Filtre: Terminacions", value=True)

# CÀLCUL MATEMÀTIC
total = 13983816
restant = total
if f_dec: restant *= 0.18
if f_suma: restant *= 0.15
if f_ab: restant *= 0.35
if f_ps: restant *= 0.35
if gem_on: restant *= 0.12
if cons_on: restant *= 0.40
if f_term: restant *= 0.80

st.markdown(f"""
    <div class="stats-box">
        TOTAL COMBINACIONS POSSIBLES: {total:,}<br>
        COMBINACIONS QUE COMPLEIXEN ELS FILTRES: <strong>{int(restant):,}</strong>
    </div>
""", unsafe_allow_html=True)

# --- GENERADOR ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES OPTIMITZADES"):
    finales = []
    # Reintegres segons lògica original (3 de [0-4] i 3 de [5-9])
    reintegres_gen = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        
        c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
        
        if len(set(c)) == 7:
            # Validacions internes
            d = [(x-1)//10 for x in c]
            cond_dec = (sorted([d.count(i) for i in range(5)], reverse=True) == [2,2,1,1,1]) if f_dec else True
            cond_sum = (150 <= sum(c) <= 220) if f_suma else True
            bajos = len([x for x in c if x<=25])
            cond_ab = (bajos == (4 if t_ab=="4B3A" else 3)) if f_ab else True
            pares = len([x for x in c if x%2==0])
            cond_ps = (pares == (4 if t_ps=="4P3S" else 3)) if f_ps else True
            gc = len([x for x in c if x in gemelos_list])
            cond_gem = (gc == 1) if u_gem else (gc == 0)
            cc = sum(1 for i in range(6) if c[i+1]-c[i] == 1)
            cond_cons = (cc == 1) if u_cons else (cc == 0)
            terms = [x % 10 for x in c]
            cond_term = all(terms.count(i) <= 2 for i in range(10)) if f_term else True
            
            if all([cond_dec, cond_sum, cond_ab, cond_ps, cond_gem, cond_cons, cond_term]):
                if not any(len(set(c) & set(ant)) > 2 for ant in finales):
                    finales.append(c)
        intents += 1

    if finales:
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{reintegres_gen[i]}</div></div>', unsafe_allow_html=True)
