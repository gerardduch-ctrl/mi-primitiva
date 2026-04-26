import streamlit as st
import random

# --- CONFIGURACIÓ ---
st.set_page_config(page_title="P - Primitiva Pro v14", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f4f4f4; border-radius: 3px; font-size: 10px; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES OFICIALS REALS ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]
bote_actual = "9.500.000 €"

# --- LÒGICA DE GRUPS ---
gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 38, 39, 47, 45, 1, 23, 14, 25, 30]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

def analitzar_v14(c, f_dec, f_suma, f_ab, f_ps, f_term, usar_gem, usar_cons):
    # 1. Decenes
    decs = [(x-1)//10 for x in c]
    if f_dec and any(decs.count(i) > 2 for i in range(5)): return False
    # 2. Suma (7 números: 150-220)
    if f_suma and not (150 <= sum(c) <= 220): return False
    # 3. Terminacions
    terms = [x % 10 for x in c]
    if f_term and any(terms.count(i) > 2 for i in range(10)): return False
    
    # 4. BESSONS (ESTRICTE)
    gc = len([x for x in c if x in gemelos_list])
    if usar_gem and gc != 1: return False
    if not usar_gem and gc > 0: return False
    
    # 5. CONSECUTIUS (ESTRICTE)
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    if usar_cons and cc != 1: return False
    if not usar_cons and cc > 0: return False
    
    return True

# --- UI ---
st.title("PRIMITIVA PRO v14")
st.markdown(f'<div class="bote-box">PROPER SORTEIG BOTE:<br>{bote_actual}</div>', unsafe_allow_html=True)

# HISTÒRIC
for s in sorteigs_reals:
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f'<div class="card"><strong>📅 {s["data"]}</strong><br>{n_html} <div class="num r-num">{s["r"]}</div></div>', unsafe_allow_html=True)

st.divider()

# PANELL CONTROL
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Màx 2 per desena", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (3 primeres)", value=True)
cons_on = st.toggle("Filtre: Consecutius (3 primeres)", value=True)
f_term = st.toggle("Filtre: Terminacions", value=True)

# GENERADOR
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚMEROS)"):
    finales = []
    rs_top = [8, 5, 2, 0, 7, 9]
    intents = 0
    while len(finales) < 6 and intents < 80000:
        # Lògica 3+3 original
        u_gem = gem_on if len(finales) < 3 else False
        u_cons = cons_on if len(finales) < 3 else False
        
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 7:
            if analitzar_v14(c, f_dec, f_suma, f_ab, f_ps, f_term, u_gem, u_cons):
                # Filtres d'alternança addicionals
                bajos = len([x for x in c if x <= 25])
                pares = len([x for x in c if x % 2 == 0])
                ok_ab = (bajos == (4 if len(finales)%2==0 else 3)) if f_ab else True
                ok_ps = (pares == (4 if len(finales)%3==0 else 3)) if f_ps else True
                
                if ok_ab and ok_ps:
                    finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("⚠️ Filtres massa estrictes. Prova de nou.")
    else:
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)

st.info("S'ha blindat el filtre de consecutius: si el botó està OFF o l'aposta és de les 3 últimes, no en sortirà cap.")
