import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Pro v13", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f4f4f4; border-radius: 3px; font-size: 10px; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES REALS VERIFICADES ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]
bote_actual = "9.500.000 €"

# --- LÒGICA DE FILTRES ---
gemelos_list = [11, 22, 33, 44]
cal_hist = [38, 39, 47, 3, 45, 30]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def analitzar_i_validar(c, f_dec, f_suma, f_ab, f_ps, f_gem, f_cons, f_term, modo_generar=False, t_ab="4B3A", t_ps="4P3S", usar_gem=True, usar_cons=True):
    res = {}
    # 1. Decenes
    decs = [(x-1)//10 for x in c]
    res['dec'] = all(decs.count(i) <= 2 for i in range(5))
    # 2. Suma (Adaptada a 7 o 6 números)
    inf, sup = (150, 220) if len(c) == 7 else (131, 160)
    res['suma'] = inf <= sum(c) <= sup
    # 3. Alts/Baixos
    bajos = [x for x in c if x <= 25]
    res['ab'] = (len(bajos) == (4 if t_ab == "4B3A" else 3)) if modo_generar else len(bajos) in [3, 4]
    # 4. Parells/Senars
    pares = len([x for x in c if x % 2 == 0])
    res['ps'] = (pares == (4 if t_ps == "4P3S" else 3)) if modo_generar else pares in [3, 4]
    # 5. Bessons
    gc = len([x for x in c if x in gemelos_list])
    res['gem'] = (gc == 1) if usar_gem else (gc == 0)
    # 6. Consecutius
    sc = sorted(c)
    cc = sum(1 for i in range(len(c)-1) if sc[i+1]-sc[i] == 1)
    res['cons'] = (cc == 1) if usar_cons else (cc == 0)
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
st.title("PRIMITIVA PRO v13")

# 1. EL BOTE
st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote_actual}</div>', unsafe_allow_html=True)

# 2. ANÀLISI HISTÒRIC AMB DIAGNÒSTIC
st.subheader("Anàlisi Històric Reial")
for s in sorteigs_reals:
    # Diagnòstic (sempre basat en filtres actius per veure ✅/❌)
    _, d = analitzar_i_validar(s['nums'], True, True, True, True, True, True, True, usar_gem=True, usar_cons=True)
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

# 3. PANELL DE CONTROL (Sota l'històric)
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Màx 2 per desena", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (3 primeres)", value=True)
cons_on = st.toggle("Filtre: Consecutius (3 primeres)", value=True)
f_term = st.toggle("Filtre: Terminacions", value=True)

# 4. GENERADOR (Múltiple de 7 números)
if st.button("GENERAR APOSTES MÚLTIPLES OPTIMITZADES"):
    finales = []
    rs_top = [8, 5, 2, 7, 0, 9]
    intentos = 0
    while len(finales) < 6 and intentos < 80000:
        t_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        t_ps = "4P3S" if len(finales) % 3 == 0 else "3P4S"
        # Respectar lògica original 3 + 3
        usar_gem = gem_on if len(finales) < 3 else False
        usar_cons = cons_on if len(finales) < 3 else False
        
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        if len(c) == 7:
            valid, _ = analitzar_i_validar(c, f_dec, f_suma, f_ab, f_ps, gem_on, cons_on, f_term, True, t_ab, t_ps, usar_gem, usar_cons)
            if valid:
                finales.append(c)
        intentos += 1

    if len(finales) < 6:
        st.warning("⚠️ Massa filtres. Prova de nou.")
    else:
        st.subheader("Les teves Apostes (7 números)")
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)
