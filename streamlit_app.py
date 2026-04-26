import streamlit as st
import random
import requests
from bs4 import BeautifulSoup

# --- 1. CONFIGURACIÓ (Sempre a dalt de tot) ---
st.set_page_config(page_title="P - Primitiva Pro v29", page_icon="P")

# --- 2. ESTILS CSS (Negreta forçada i minimalisme) ---
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    div[data-testid="stWidgetLabel"] p, label p { color: black !important; font-weight: 900 !important; font-size: 16px !important; }
    .card { padding: 12px; border: 2px solid black; margin-bottom: 10px; background-color: #fff; text-align: center; }
    .num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; border: 2px solid black; margin: 2px; font-weight: bold; font-size: 13px; text-align: center; color: black; }
    .r-num { background-color: black; color: white; }
    .diag-box { margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 10px; line-height: 1.4; color: #333; font-weight: bold; }
    .bote-box { background-color: #000; color: gold; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border: 4px solid gold; margin-bottom: 20px; }
    .stButton>button { background-color: black !important; color: white !important; width: 100%; height: 60px; font-weight: bold; font-size: 20px; border: 2px solid gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DADES INICIALS I GRUPS ---
if 'sorteigs' not in st.session_state:
    st.session_state.sorteigs = [
        {"data": "Dissabte 25/04/2026", "nums": [3, 6, 10, 28, 30, 46], "r": "1"},
        {"data": "Dijous 23/04/2026", "nums": [11, 13, 20, 26, 27, 34], "r": "8"},
        {"data": "Dilluns 20/04/2026", "nums": [4, 7, 29, 39, 41, 48], "r": "7"}
    ]
    st.session_state.bote = "9.500.000 €"

gemelos_list = [11, 22, 33, 44]
cal_hist = [3, 23, 30, 38, 39, 47]
n_tots = list(range(1, 50))
desp_hist = [x for x in n_tots if x not in cal_hist][:20]
hielo_hist = [x for x in n_tots if x not in cal_hist and x not in desp_hist]

# --- 4. FUNCIONS DE SUPORT ---
def analitzar_total(c):
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
    t = [x % 10 for x in c]
    ok_t = all(t.count(i) <= 2 for i in range(10))
    return [
        f"{'✅' if counts == target else '❌'} Dec",
        f"{'✅' if l_inf <= s_tot <= l_sup else '❌'} Sum ({s_tot})",
        f"{'✅' if bajos in [3,4] else '❌'} A/B",
        f"{'✅' if pares in [3,4] else '❌'} P/S",
        f"{'✅' if gc == 1 else '❌'} Bes",
        f"{'✅' if cc == 1 else '❌'} Cons",
        f"{'✅' if ok_t else '❌'} Term"
    ]

def actualitzar_online():
    try:
        res = requests.get("https://loteriasyapuestas.es", timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        new_sorteigs = []
        items = soup.select('.c-cuerpo-reparto-premios')
        for item in items[:3]:
            data = item.select_one('.c-cuerpo-reparto-premios__fecha').text.strip()
            bolas = [int(n.text.strip()) for n in item.select('.c-cuerpo-reparto-premios__combinacion-numero')][:6]
            r = item.select_one('.c-cuerpo-reparto-premios__combinacion-reintegro').text.strip()
            new_sorteigs.append({"data": data, "nums": sorted(bolas), "r": r})
        bote = soup.select_one('.c-anuncio-proximo-sorteo__importe').text.strip()
        return new_sorteigs, bote
    except:
        return None, None

# --- 5. UI: BOTE I HISTÒRIC ---
st.markdown(f'<div class="bote-box">BOTE ACTUAL:<br>{st.session_state.bote}</div>', unsafe_allow_html=True)

if st.button("🔄 ACTUALITZAR DADES ONLINE"):
    with st.spinner("Connectant..."):
        s, b = actualitzar_online()
        if s:
            st.session_state.sorteigs, st.session_state.bote = s, b
            st.success("Dades actualitzades!")
        else:
            st.error("Error de connexió.")

for s in st.session_state.sorteigs:
    diag = analitzar_total(s['nums'])
    n_html = "".join([f'<div class="num">{x}</div>' for x in s['nums']])
    st.markdown(f"""
        <div class="card">
            <strong>📅 {s['data']}</strong><br>{n_html} <div class="num r-num">{s['r']}</div>
            <div class="diag-box">{" | ".join(diag)}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 6. PANELL CONTROL ---
f_dec = st.toggle("Filtre: Decenes 2-2-1-1-1", value=True)
f_suma = st.toggle("Filtre: Suma equilibrada", value=True)
f_ab = st.toggle("Filtre: Alts/Baixos", value=True)
f_ps = st.toggle("Filtre: Parells/Senars", value=True)
gem_on = st.toggle("Filtre: Bessons (Apostes 1, 2, 3)", value=True)
cons_on = st.toggle("Filtre: Consecutius (Apostes 1, 3, 5)", value=True)
f_term = st.toggle("Filtre: Terminacions", value=True)

# --- 7. GENERADOR (7 NÚMEROS I REINTEGRE 3+3) ---
if st.button("GENERAR 6 APOSTES MÚLTIPLES (7 NÚM)"):
    finales = []
    rs_orig = random.sample(range(5), 3) + random.sample(range(5, 10), 3)
    intents = 0
    while len(finales) < 6 and intents < 100000:
        idx = len(finales)
        t_ab = "4B3A" if idx % 2 == 0 else "3B4A"
        t_ps = "4P3S" if idx % 2 == 0 else "3P4S"
        u_gem = gem_on if idx < 3 else False
        u_cons = cons_on if idx in [0, 2, 4] else False
        
        c = sorted(random.sample(cal_hist, 1) + random.sample(desp_hist, 4) + random.sample(hielo_hist, 2))
        
        if len(set(c)) == 7:
            d = [(x-1)//10 for x in c]
            if f_dec and sorted([d.count(i) for i in range(5)], reverse=True) != [2,2,1,1,1]: continue
            if f_suma and not (150 <= sum(c) <= 220): continue
            bajos = len([x for x in c if x <= 25])
            if f_ab and bajos != (4 if t_ab == "4B3A" else 3): continue
            gc = len([x for x in c if x in gemelos_list])
            if (u_gem and gc != 1) or (not u_gem and gc > 0): continue
            cc = sum(1 for i in range(6) if c[i+1]-c[i] == 1)
            if (u_cons and cc != 1) or (not u_cons and cc > 0): continue
            if any(len(set(c) & set(ant)) > 2 for ant in finales): continue
            
            finales.append(c)
        intents += 1

    if finales:
        for i, combo in enumerate(finales):
            n_html = "".join([f'<div class="num">{x}</div>' for x in combo])
            st.markdown(f'<div class="card">{n_html} <div class="num r-num">{rs_orig[i]}</div></div>', unsafe_allow_html=True)
