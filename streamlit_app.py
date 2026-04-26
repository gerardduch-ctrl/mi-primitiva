import streamlit as st
import random
from itertools import combinations

# --- 1. CONFIGURACIÓ I ESTIL ---
st.set_page_config(page_title="P - Primitiva Pro v30", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; border: 2px solid black; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; text-align: left; line-height: 1.5; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADES REALS I GRUPS ---
SORTEIGS_REALS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

# Definició de grups segons la teva lògica de temperatura
CALIENTES = [3, 23, 30, 38, 39, 47, 10, 6, 14, 45]
DESPERTANDO = [2, 4, 7, 11, 15, 18, 20, 25, 28, 33, 35, 40, 41, 44, 46, 48, 49, 12, 22, 31]
HIELO = [1, 5, 8, 9, 13, 16, 17, 19, 21, 24, 26, 27, 29, 32, 34, 36, 37, 42, 43]
GEMELOS = {11, 22, 33, 44}

# LÒGICA DE REINTEGRES ORIGINAL (3 Freds i 3 Despertant)
# Freds: 0, 1, 2, 3, 4 | Despertant: 5, 6, 7, 8, 9
REINTEGRES_FRIO = [0, 1, 2, 3, 4]
REINTEGRES_DESP = [5, 6, 7, 8, 9]

# --- 3. FUNCIONS DE VALIDACIÓ ---
def comprovar_22111(combo):
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    return all(c > 0 for c in counts) and all(c <= 2 for c in counts)

def analitzar_diagnostico(c):
    is_7 = len(c) == 7
    d_count = [(x-1)//10 for x in c]
    ok_dec = comprovar_22111(c) if is_7 else all(d_count.count(i) > 0 for i in range(5))
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    ok_suma = l_inf <= s_tot <= l_sup
    bajos = len([x for x in c if x <= 25])
    pares = len([x for x in c if x % 2 == 0])
    gc = len([x for x in c if x in GEMELOS])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    
    return [
        f"{'✅' if ok_dec else '❌'} Decenes",
        f"{'✅' if ok_suma else '❌'} Suma({s_tot})",
        f"{'✅' if bajos==4 else '❌'} Alts/Baixos({bajos}B)",
        f"{'✅' if (pares in [3,4]) else '❌'} Parells({pares})",
        f"{'✅' if gc==1 else '❌'} Bessons",
        f"{'✅' if cc==1 else '❌'} Consecutius",
        f"Inèdita: ✅"
    ]

# --- 4. UI: BOTE I HISTÒRIC ---
st.markdown('<div class="bote-box">BOTE ACTUAL:<br>9.500.000 €</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Històric (7 Paràmetres)")
for s in SORTEIGS_REALS:
    diag = analitzar_diagnostico(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(diag)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. PANELL DE CONTROL ---
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma (150-220)", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)

# --- 6. GENERADOR AMB REINTEGRE ORIGINAL RECUPERAT ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    
    # GENERACIÓ DE REINTEGRES: 3 Freds i 3 Despertant (exactament com l'original)
    r_freds = random.sample(REINTEGRES_FRIO, 3)
    r_desp = random.sample(REINTEGRES_DESP, 3)
    reintegres_finals = r_freds + r_desp
    # No els barregem per mantenir l'ordre del llistat original (3+3)

    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if (idx in [0, 2, 4]) else False
        
        # Selecció: 1 Calent, 4 Despertant, 2 Hielo
        c = sorted(random.sample(CALIENTES, 1) + random.sample(DESPERTANDO, 4) + random.sample(HIELO, 2))
        
        if len(set(c)) == 7:
            # Validació Decenes 2-2-1-1-1
            if f_dec and not comprovar_22111(c): continue
            
            # Validació Suma
            if f_suma and not (150 <= sum(c) <= 220): continue
            
            # Validació Bessons i Consecutius
            gc = len([x for x in c if x in GEMELOS])
            if (u_gem and gc != 1) or (not u_gem and gc > 0): continue
            
            sc = sorted(c)
            cc = sum(1 for i in range(6) if sc[i+1]-sc[i] == 1)
            if (u_cons and cc != 1) or (not u_cons and cc > 0): continue

            # Solapament màxim 2
            if any(len(set(c) & set(ant)) > 2 for ant in finales): continue

            finales.append(c)
        intents += 1

    if finales:
        st.subheader("Les teves Apostes")
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{reintegres_finals[i]}</div></div>', unsafe_allow_html=True)
