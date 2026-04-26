import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="P - Primitiva Total Control", page_icon="P")

st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 5px; background: #f9f9f9; border-radius: 3px; font-size: 11px; line-height: 1.4; }
    .bote-box { background-color: #000; color: gold; padding: 15px; text-align: center; font-size: 22px; font-weight: 900; border: 3px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 50px; font-weight: bold; border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- DADES OFICIALS REALS (Abril 2026) ---
sorteigs_reals = [
    {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
    {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
    {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
]

# --- LÒGICA DE GRUPS ---
gemelos_list = [11, 22, 33, 44]
cal_hist = [38, 39, 47, 3, 45]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

# --- FUNCIÓ DE DIAGNÒSTIC I VALIDACIÓ ---
def analitzar_i_validar(c, f_dec, f_suma, f_ab, f_gem, f_cons, modo_generar=False, t_ab="4B3A"):
    res = {}
    # 1. Decenes (Máx 2)
    decs = [(x-1)//10 for x in c]
    res['dec'] = all(decs.count(i) <= 2 for i in range(5))
    
    # 2. Suma (Adaptada a 7 números si es genera, o normal si s'analitza)
    s_total = sum(c)
    limit_inf, limit_sup = (150, 220) if len(c) == 7 else (131, 160)
    res['suma'] = limit_inf <= s_total <= limit_sup
    res['suma_val'] = s_total
    
    # 3. Alts/Baixos
    bajos = [x for x in c if x <= 25]
    if modo_generar:
        res['ab'] = (t_ab == "4B3A" and len(bajos) == 4) or (t_ab == "3B4A" and len(bajos) == 3)
    else:
        res['ab'] = len(bajos) in [3, 4]
    res['ab_val'] = f"{len(bajos)}B/{len(c)-len(bajos)}A"
    
    # 4. Bessons
    gc = len([x for x in c if x in gemelos_list])
    res['gem'] = (gc == 1) if f_gem else (gc == 0)
    res['gem_val'] = gc
    
    # 5. Consecutius
    sc = sorted(c)
    cc = sum(1 for i in range(len(c)-1) if sc[i+1]-sc[i] == 1)
    res['cons'] = (cc == 1) if f_cons else (cc == 0)
    res['cons_val'] = cc

    # Check final segons filtres activats
    valid = True
    if f_dec and not res['dec']: valid = False
    if f_suma and not res['suma']: valid = False
    if f_ab and not res['ab']: valid = False
    if f_gem and not res['gem']: valid = False
    if f_cons and not res['cons']: valid = False
    
    return valid, res

# --- INTERFÍCIE ---
st.title("PRIMITIVA TOTAL CONTROL v9")

# 1. BOTE I CONFIGURACIÓ DE FILTRES
st.markdown('<div class="bote-box">BOTE ACTUAL: 9.500.000 €</div>', unsafe_allow_html=True)

with st.expander("⚙️ CONFIGURACIÓ DE FILTRES (Activa/Desactiva)", expanded=True):
    f_dec = st.toggle("Filtre: Màx 2 per desena", value=True)
    f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
    f_ab = st.toggle("Filtre: Alternança Alts/Baixos", value=True)
    f_gem = st.toggle("Filtre: Un número Bessó", value=True)
    f_cons = st.toggle("Filtre: Una parella Consecutiva", value=True)

# 2. ANÀLISI HISTÒRIC AMB DIAGNÒSTIC
st.subheader("Anàlisi Històric")
for s in sorteigs_reals:
    _, d = analitzar_i_validar(s['nums'], f_dec, f_suma, f_ab, f_gem, f_cons)
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">
                {'✅' if d['dec'] else '❌'} Decenes | 
                {'✅' if d['suma'] else '❌'} Suma ({d['suma_val']}) | 
                {'✅' if d['ab'] else '❌'} A/B ({d['ab_val']}) | 
                {'✅' if d['gem'] else '❌'} Bessons ({d['gem_val']}) | 
                {'✅' if d['cons'] else '❌'} Cons ({d['cons_val']})
            </div>
        </div>
    """, unsafe_allow_html=True)

# 3. GENERADOR
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚMEROS)"):
    finales = []
    rs_top = [8, 5, 2, 0, 7, 1]
    intents = 0
    while len(finales) < 6 and intents < 60000:
        t_ab = "4B3A" if len(finales) % 2 == 0 else "3B4A"
        # Generació base 7 números
        c = random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2)
        c = sorted(list(set(c)))
        
        if len(c) == 7:
            es_valida, _ = analitzar_i_validar(c, f_dec, f_suma, f_ab, f_gem, f_cons, True, t_ab)
            if es_valida:
                finales.append(c)
        intents += 1

    if len(finales) < 6:
        st.warning("Filtres massa estrictes. Desactiva algun filtre per generar.")
    else:
        st.subheader("Les teves Apostes Múltiples (7 números)")
        for idx, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html}<div class="num r-num">{rs_top[idx]}</div></div>', unsafe_allow_html=True)

st.divider()
st.info("Pots activar o desactivar cada filtre individualment des del menú de configuració superior.")
