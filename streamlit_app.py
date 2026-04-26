import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro v11", page_icon="P", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f4f4f4; border-radius: 3px; font-size: 10px; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 15px; text-align: center; font-size: 22px; font-weight: 900; border: 3px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; border-radius: 0px; font-size: 20px; border: 2px solid gold !important; }
    .prob-box { background-color: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; margin: 15px 0; font-weight: bold; text-align: center; color: #856404; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES OFICIALS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 38, 39, 47, 45, 1, 2, 10, 23, 30]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

# --- FUNCIÓ DE DIAGNÒSTIC I VALIDACIÓ ---
def analitzar_i_validar(c, f_dec, f_suma, f_ab, f_ps, f_gem, f_cons, f_term, modo_generar=False, t_ab="4B3A", t_ps="4P3S"):
    res = {}
    # 1. Decenes
    decs = [(x-1)//10 for x in c]
    res['dec'] = all(decs.count(i) <= 2 for i in range(5))
    # 2. Suma
    s_total = sum(c)
    inf, sup = (150, 220) if len(c) == 7 else (131, 160)
    res['suma'] = inf <= s_total <= sup
    # 3. Alts/Baixos
    bajos = [x for x in c if x <= 25]
    res['ab'] = (len(bajos) == (4 if t_ab == "4B3A" else 3)) if modo_generar else len(bajos) in [3, 4]
    # 4. Parells/Senars
    pares = len([x for x in c if x % 2 == 0])
    res['ps'] = (pares == (4 if t_ps == "4P3S" else 3)) if modo_generar else pares in [3, 4]
    # 5. Bessons
    gc = len([x for x in c if x in gemelos_list])
    res['gem'] = (gc == 1) if f_gem else (gc == 0)
    # 6. Consecutius
    sc = sorted(c)
    cc = sum(1 for i in range(len(c)-1) if sc[i+1]-sc[i] == 1)
    res['cons'] = (cc == 1) if f_cons else (cc == 0)
    # 7. Terminacions
    terms = [x % 10 for x in c]
    res['term'] = all(terms.count(i) <= 2 for i in range(10))

    valid = True
    if f_dec and not res['dec']: valid = False
    if f_suma and not res['suma']: valid = False
    if f_ab and not res['ab']: valid = False
    if f_ps and not res['ps']: valid = False
    if f_gem and not res['gem']: valid = False
    if f_cons and not res['cons']: valid = False
    if f_term and not res['term']: valid = False
    
    return valid, res

# --- UI ---
st.title("SISTEMA PRM PRO v11")
st.markdown('<div class="bote-box">BOTE ACTUAL: 9.500.000 €</div>', unsafe_allow_html=True)

# 1. RESULTATS I COMPROVACIONS
st.subheader("Anàlisi Històric Reial")
for s in sorteigs_reals:
    # Per l'anàlisi històric activem tot per veure el diagnòstic complet
    _, d = analitzar_i_validar(s['nums'], True, True, True, True, True, True, True)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">
                {'✅' if d['dec'] else '❌'} Dec | {'✅' if d['suma'] else '❌'} Suma | 
                {'✅' if d['ab'] else '❌'} A/B | {'✅' if d['ps'] else '❌'} P/S |
                {'✅' if d['gem'] else '❌'} Bes | {'✅' if d['cons'] else '❌'} Cons | 
                {'✅' if d['term'] else '❌'} Term
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# 2. PANELL DE CONTROL (Sota els resultats)
st.subheader("⚙️ Panell de Control de Filtres")
f_dec = st.toggle("Filtre: Màx 2 per desena", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alternança Alts/Baixos (4/3)", value=True)
f_ps = st.toggle("Filtre: Alternança Parells/Senars (4/3)", value=True)
f_gem = st.toggle("Filtre: Un número Bessó (11,22,33,44)", value=True)
f_cons = st.toggle("Filtre: Una parella Consecutiva", value=True)
f_term = st.toggle("Filtre: Terminacions (Màx 2 iguals)", value=True)

# 3. CÀLCUL DINÀMIC DE PROBABILITATS
total_combis = 13983816
# Estimació matemàtica simplificada segons filtres actius
percentatge = 100.0
if f_dec: percentatge *= 0.28
if f_suma: percentatge *= 0.15
if f_ab: percentatge *= 0.35
if f_ps: percentatge *= 0.35
if f_gem: percentatge *= 0.12
if f_cons: percentatge *= 0.40
if f_term: percentatge *= 0.80

combis_restants = int(total_combis * (percentatge / 100))
if combis_restants < 1: combis_restants = 1

st.markdown(f"""
    <div class="prob-box">
        🔍 Amb els filtres seleccionats, estàs filtrant el {percentatge:.4f}% de les combinacions.<br>
        Queden <strong>{combis_restants:,}</strong> combinacions possibles de 13.983.816.
    </div>
""", unsafe_allow_html=True)

# 4. GENERADOR
if st.button("GENERAR APOSTES MÚLTIPLES OPTIMITZADES"):
    finales = []
    rs_top = [8, 5, 2, 7, 0, 9]
    intents = 0
    while len(finales) < 6 and intents < 60000:
        t_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        t_ps = "4P3S" if len(finales) % 3 == 0 else "3P4S"
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        if len(c) == 7:
            valid, _ = analitzar_i_validar(c, f_dec, f_suma, f_ab, f_ps, f_gem, f_cons, f_term, True, t_ab, t_ps)
            if valid:
                finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("⚠️ Els filtres són tan estrictes que no trobem combinacions. Desactiva'n algun.")
    else:
        st.subheader("Les teves Apostes de 7 Números")
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)

st.divider()
st.caption("v11 | Filtres dinàmics i càlcul de probabilitat en temps real.")
