import streamlit as st
import random
from itertools import combinations

# --- 1. CONFIGURACIÓ I ESTIL ---
st.set_page_config(page_title="P - Primitiva Pro v29", page_icon="P")

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

# --- 2. DADES REALS I GRUPS ---
SORTEIGS_REALS = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

# Grups originals
CALIENTES = [3, 23, 30, 38, 39, 47, 49, 1, 2, 7]
DESPERTANDO = [5, 8, 12, 15, 18, 21, 24, 27, 31, 34, 37, 40, 43, 46, 10, 14, 17, 20, 25, 29]
HIELO = [4, 6, 9, 13, 16, 19, 26, 28, 32, 35, 41, 42, 45, 48, 11, 22, 33, 44]

# LÒGICA REINTEGRES ORIGINAL (3 Freds / 3 Despertant)
R_FRIO = [0, 1, 2, 3, 4]
R_DESPERTANDO = [5, 6, 7, 8, 9]

GEMELOS = {11, 22, 33, 44}

# --- 3. FUNCIONS DE BLINDATGE ---
def comprovar_regla_22111(combo):
    """Blinda que estiguin les 5 desenes i cap tingui més de 2 números (per a 7 núms)"""
    decs = [(x-1)//10 for x in combo]
    counts = [decs.count(i) for i in range(5)]
    # Totes les desenes han de tenir almenys 1 (cap buida)
    # Cap desena pot tenir més de 2 (patró 2-2-1-1-1 per a 7 números)
    return all(c > 0 for c in counts) and all(c <= 2 for c in counts)

def analitzar_diagnostico(c):
    is_7 = len(c) == 7
    # Regla desenes adaptada: si és 6 núms (històric), almenys no buides
    d_count = [(x-1)//10 for x in c]
    ok_dec = all(d_count.count(i) > 0 for i in range(5)) if not is_7 else comprovar_regla_22111(c)
    
    s_tot = sum(c)
    l_inf, l_sup = (150, 220) if is_7 else (131, 160)
    ok_suma = l_inf <= s_tot <= l_sup
    
    bajos = len([x for x in c if x <= 25])
    ok_ab = (bajos == 4)
    
    pares = len([x for x in c if x % 2 == 0])
    sc = sorted(c)
    cc = sum(1 for i in range(len(sc)-1) if sc[i+1]-sc[i] == 1)
    gc = len([x for x in c if x in GEMELOS])

    return [
        f"{'✅' if ok_dec else '❌'} Decenes(22111)",
        f"{'✅' if ok_suma else '❌'} Suma({s_tot})",
        f"{'✅' if bajos==4 else '❌'} A/B({bajos}B)",
        f"{'✅' if gc==1 else '❌'} Bes",
        f"{'✅' if cc==1 else '❌'} Cons",
        f"P/S: {pares}P"
    ]

# --- 4. UI: BOTE I HISTÒRIC ---
st.markdown('<div class="bote-box">BOTE ACTUAL:<br>9.500.000 €</div>', unsafe_allow_html=True)

st.subheader("Anàlisi Històric amb Blindatge 2-2-1-1-1")
for s in SORTEIGS_REALS:
    checks = analitzar_diagnostico(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(checks)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. PANELL DE CONTROL ---
st.subheader("⚙️ Configuració de Filtres")
f_dec = st.toggle("Filtre: Decenes (Blindat 2-2-1-1-1)", value=True)
f_suma = st.toggle("Filtre: Suma Equilibrada", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)

# --- 6. GENERADOR (BLINDAT) ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    # Reintegre Original: 3 Freds i 3 Despertant
    rs_final = random.sample(R_FRIO, 3) + random.sample(R_DESPERTANDO, 3)
    random.shuffle(rs_final)
    
    intents = 0
    while len(finales) < 6 and intents < 150000:
        idx = len(finales)
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if (idx in [0, 2, 4]) else False
        
        # Selecció Temperatura: 1 Cal + 4 Desp + 2 Hielo
        c = sorted(random.sample(CALIENTES, 1) + random.sample(DESPERTANDO, 4) + random.sample(HIELO, 2))
        
        # BLINDATGE DESENES: Obligatori 2-2-1-1-1
        if f_dec and not comprovar_regla_22111(c): continue
        
        # Filtre Suma (7 números)
        if f_suma and not (150 <= sum(c) <= 220): continue
        
        # Bessons i Consecutius Asimètrics
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
        st.subheader("Les teves Apostes de 7 Números")
        for i, f in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in f])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs_final[i]}</div></div>', unsafe_allow_html=True)
