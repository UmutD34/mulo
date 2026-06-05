import streamlit as st
import json
import random
import urllib.parse

st.set_page_config(
    page_title="POMEM OPS",
    page_icon="🚔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Share+Tech+Mono&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)

st.markdown("""<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp {
    background-color: #0b0d11 !important;
    color: #e8edf2 !important;
    font-family: 'Noto Sans', sans-serif !important;
}
.block-container { padding: 1.2rem 0.9rem 4rem !important; max-width: 720px !important; }

/* HUD */
.hud-wrap {
    display:flex; align-items:center; justify-content:space-between;
    background:#13171f; border:1px solid #252b36; border-radius:14px;
    padding:13px 18px; margin-bottom:14px; position:relative; overflow:hidden;
}
.hud-wrap::after {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    animation: siren 0.7s steps(1) infinite;
}
@keyframes siren {
    0%  { background: linear-gradient(90deg,#ff2020 0%,#ff2020 49%,#333 50%,#1a6fff 51%,#1a6fff 100%); box-shadow:0 0 12px #ff2020; }
    50% { background: linear-gradient(90deg,#1a6fff 0%,#1a6fff 49%,#333 50%,#ff2020 51%,#ff2020 100%); box-shadow:0 0 12px #1a6fff; }
}
.hud-title { font-family:'Rajdhani',sans-serif; font-size:20px; font-weight:700; color:#4da3ff; letter-spacing:3px; text-transform:uppercase; }
.hud-sub   { font-family:'Share Tech Mono',monospace; font-size:9px; color:#4a5568; letter-spacing:2px; margin-top:3px; }
.hud-pill  { background:#0b0d11; border:1px solid #252b36; border-radius:8px; padding:5px 14px; text-align:center; }
.pill-val  { font-family:'Rajdhani',sans-serif; font-size:20px; font-weight:700; color:#f0883e; }
.pill-lbl  { font-family:'Share Tech Mono',monospace; font-size:9px; color:#4a5568; letter-spacing:1px; }

/* Stat */
.stat-row { display:flex; gap:8px; margin-bottom:14px; }
.stat-box { flex:1; background:#13171f; border:1px solid #252b36; border-radius:10px; padding:10px 8px; text-align:center; }
.stat-val { font-family:'Rajdhani',sans-serif; font-size:24px; font-weight:700; line-height:1; }
.stat-lbl { font-family:'Share Tech Mono',monospace; font-size:9px; color:#6b7280; letter-spacing:1px; margin-top:3px; }
.c-blue{color:#4da3ff} .c-green{color:#3fb950} .c-orange{color:#f0883e}

/* Progress */
.prog-wrap { margin-bottom:14px; }
.prog-meta { display:flex; justify-content:space-between; font-family:'Share Tech Mono',monospace; font-size:10px; color:#6b7280; margin-bottom:5px; }
.prog-track { background:#13171f; border-radius:4px; height:5px; border:1px solid #252b36; overflow:hidden; }
.prog-fill  { height:100%; border-radius:4px; background:linear-gradient(90deg,#1d5db5,#4da3ff); transition:width .5s ease; }

/* Soru kartı */
.q-card {
    background:#13171f; border:1px solid #252b36; border-radius:14px;
    padding:24px 20px 18px; margin-bottom:14px; position:relative; overflow:hidden;
    animation:up .3s ease;
}
@keyframes up { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.q-card::before { content:''; position:absolute; left:0;top:0;bottom:0; width:4px; background:linear-gradient(180deg,#4da3ff,#1d5db5); border-radius:4px 0 0 4px; }
.q-tag { font-family:'Share Tech Mono',monospace; font-size:9px; color:#4a5568; letter-spacing:3px; text-transform:uppercase; margin-bottom:10px; display:flex; align-items:center; gap:8px; }
.q-id  { background:#0b0d11; border:1px solid #252b36; border-radius:4px; padding:2px 7px; font-size:9px; color:#4da3ff; }
.q-text { font-family:'Noto Sans',sans-serif; font-size:17px; font-weight:700; color:#f0f4f8; line-height:1.5; }
.q-foot { margin-top:12px; font-family:'Share Tech Mono',monospace; font-size:9px; color:#4a5568; letter-spacing:2px; }
.q-foot span { color:#f0883e; }

/* Cevap */
.a-card {
    background:#0e1a13; border:1px solid #2a5c39; border-radius:14px;
    padding:20px; margin-bottom:12px; position:relative; overflow:hidden;
    animation:reveal .35s ease;
}
@keyframes reveal { from{opacity:0;transform:scaleY(.93);transform-origin:top} to{opacity:1;transform:scaleY(1)} }
.a-card::before { content:''; position:absolute; left:0;top:0;bottom:0; width:4px; background:linear-gradient(180deg,#3fb950,#238636); border-radius:4px 0 0 4px; }
.a-head { font-family:'Share Tech Mono',monospace; font-size:9px; color:#3fb950; letter-spacing:3px; margin-bottom:10px; }
.a-body { font-family:'Noto Sans',sans-serif; font-size:15px; color:#d0dce8; line-height:1.8; white-space:pre-line; }

/* Ödül */
.reward-banner {
    border-radius:10px; padding:11px 16px; margin-bottom:12px;
    font-family:'Rajdhani',sans-serif; font-size:15px; font-weight:700;
    letter-spacing:2px; text-align:center; text-transform:uppercase; animation:up .3s ease;
}
.reward-green  { background:#0e1a13; border:1px solid #3fb950; color:#3fb950; }
.reward-orange { background:#1a1208; border:1px solid #f0883e; color:#f0883e; }
.reward-blue   { background:#0b1320; border:1px solid #4da3ff; color:#4da3ff; }

/* ── Buton Grid — HTML tabanlı, Streamlit column'larından bağımsız ── */
.btn-grid {
    display: grid;
    grid-template-columns: 1fr 1.5fr 1fr 1fr;
    gap: 8px;
    margin-bottom: 10px;
}
.btn-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}
.hbtn {
    display: flex; align-items: center; justify-content: center;
    height: 46px; border-radius: 8px; cursor: pointer;
    font-family: 'Rajdhani', sans-serif; font-weight: 700;
    font-size: 13px; letter-spacing: 2px; text-transform: uppercase;
    text-decoration: none; border: 1px solid #252b36;
    background: #13171f; color: #adb5bd;
    transition: all .2s; white-space: nowrap;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
}
.hbtn:active { transform: scale(.96); }
.hbtn.blue  { border-color:#2a4a7f; color:#4da3ff; }
.hbtn.green { border-color:#2a5c39; color:#3fb950; }
.hbtn.orange{ border-color:#7a3f10; color:#f0883e; }
.hbtn.red   { border-color:#5a1f1f; color:#f87171; }
.hbtn.gray  { border-color:#252b36; color:#6b7280; }

/* Streamlit butonları — sadece expander içi için */
.stButton > button {
    font-family:'Rajdhani',sans-serif !important; font-weight:700 !important;
    font-size:12px !important; letter-spacing:1px !important;
    text-transform:uppercase !important; border-radius:8px !important;
    height:40px !important; width:100% !important;
    background:#13171f !important; border:1px solid #252b36 !important;
    color:#adb5bd !important; transition:all .2s !important;
}
.stButton > button:hover:not(:disabled) { background:#1a1f2b !important; border-color:#4da3ff !important; color:#4da3ff !important; }
.stButton > button:disabled { opacity:.25 !important; }

.stSelectbox > div > div { background:#13171f !important; border-color:#252b36 !important; color:#e8edf2 !important; font-family:'Share Tech Mono',monospace !important; font-size:12px !important; border-radius:8px !important; }
.stSelectbox label, .stNumberInput label { color:#6b7280 !important; font-family:'Share Tech Mono',monospace !important; font-size:10px !important; letter-spacing:2px !important; }
.stNumberInput input { background:#13171f !important; border-color:#252b36 !important; color:#e8edf2 !important; font-family:'Share Tech Mono',monospace !important; }

details > summary { background:#13171f !important; border:1px solid #252b36 !important; border-radius:8px !important; color:#6b7280 !important; font-family:'Share Tech Mono',monospace !important; font-size:11px !important; letter-spacing:2px !important; padding:12px 16px !important; list-style:none; }
details[open] > summary { border-radius:8px 8px 0 0 !important; }
details > div { background:#0f1318 !important; border:1px solid #252b36 !important; border-top:none !important; border-radius:0 0 8px 8px !important; }

#MainMenu,footer,header { visibility:hidden !important; }
[data-testid="stDecoration"] { display:none !important; }
hr { border:none; border-top:1px solid #1e2530 !important; margin:14px 0 !important; }

/* Mobil fine-tuning */
@media (max-width:480px) {
    .hud-title { font-size:17px; }
    .q-text    { font-size:16px; }
    .a-body    { font-size:14px; }
    .stat-val  { font-size:21px; }
    .btn-grid  { grid-template-columns: 1fr 1.5fr 1fr 1fr; gap:6px; }
    .hbtn      { font-size:11px; height:44px; letter-spacing:1px; }
    .block-container { padding:1rem .6rem 3rem !important; }
}
</style>""", unsafe_allow_html=True)


# ── Veri ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    for fname in ("sorular.json", "pomem_sorular_unique.json", "pomem_sorular.json"):
        try:
            with open(fname, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            continue
    return [{"id":1,"soru":"sorular.json bulunamadı.","cevap":"Dosya yolunu kontrol et.","donem":"—"}]

data     = load_data()
donemler = sorted(set(q.get("donem","—") for q in data))

REWARDS = {
    1:   ("🎯 İLK CEVAP!", "green"),
    5:   ("⚡ 5 SORU TAMAM!", "blue"),
    10:  ("🔥 10 SORUDA!", "orange"),
    25:  ("💥 25 SORU — CANAVAR!", "orange"),
    50:  ("🏆 50 SORU — EFSANESİN!", "orange"),
    100: ("👑 100 SORU — POMEM'E HAZIRSIN!", "orange"),
}

# ── Session State ─────────────────────────────────────────────────────────────
for k, v in [("index",0),("show_ans",False),("seen",0),
             ("mode","sıralı"),("filter_donem","Tümü"),
             ("filtered_data",data),("reward",""),("reward_type","green")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Yardımcılar ──────────────────────────────────────────────────────────────
def get_filtered():
    fd = st.session_state.filter_donem
    return data if fd == "Tümü" else [q for q in data if q.get("donem","—") == fd]

filtered = st.session_state.filtered_data or data
idx      = max(0, min(st.session_state.index, len(filtered)-1))
q        = filtered[idx]


# ── HUD ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hud-wrap">
  <div>
    <div class="hud-title">🚔 POMEM OPS</div>
    <div class="hud-sub">MÜLAKAT SİMÜLATÖRÜ · AKTİF</div>
  </div>
  <div class="hud-pill">
    <div class="pill-val">{len(filtered)}</div>
    <div class="pill-lbl">SORU</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
  <div class="stat-box"><div class="stat-val c-blue">{idx+1}</div><div class="stat-lbl">Şu an</div></div>
  <div class="stat-box"><div class="stat-val c-green">{st.session_state.seen}</div><div class="stat-lbl">Görülen</div></div>
  <div class="stat-box"><div class="stat-val c-orange">{len(data)}</div><div class="stat-lbl">Toplam</div></div>
</div>""", unsafe_allow_html=True)

# ── Progress ──────────────────────────────────────────────────────────────────
pct = round((idx+1)/len(filtered)*100, 1)
st.markdown(f"""
<div class="prog-wrap">
  <div class="prog-meta"><span>İLERLEME</span><span>{idx+1} / {len(filtered)} · %{pct}</span></div>
  <div class="prog-track"><div class="prog-fill" style="width:{pct}%"></div></div>
</div>""", unsafe_allow_html=True)

# ── Filtreler ─────────────────────────────────────────────────────────────────
with st.expander("⚙️  FİLTRELER & AYARLAR"):
    ca, cb = st.columns(2)
    with ca:
        new_d = st.selectbox("DÖNEM", ["Tümü"]+donemler,
            index=(["Tümü"]+donemler).index(st.session_state.filter_donem))
        if new_d != st.session_state.filter_donem:
            st.session_state.filter_donem  = new_d
            st.session_state.filtered_data = get_filtered()
            st.session_state.index = 0
            st.session_state.show_ans = False
            st.session_state.reward = ""
            st.rerun()
    with cb:
        jump = st.number_input("ATLA", min_value=1, max_value=len(filtered), value=idx+1, step=1)
        if st.button("🎯  GİT"):
            st.session_state.index    = jump-1
            st.session_state.show_ans = False
            st.session_state.reward   = ""
            st.rerun()

    mc1, mc2 = st.columns(2)
    with mc1:
        if st.button("📋  SIRALI"):
            st.session_state.mode = "sıralı"; st.rerun()
    with mc2:
        if st.button("🔀  RASTGELE"):
            st.session_state.mode = "rastgele"; st.rerun()
    mode_txt = "📋 SIRALI" if st.session_state.mode == "sıralı" else "🔀 RASTGELE"
    st.markdown(
        f"<div style='font-family:Share Tech Mono,monospace;font-size:10px;"
        f"color:#4a5568;letter-spacing:2px;padding-top:6px'>"
        f"AKTİF MOD · <span style='color:#4da3ff'>{mode_txt}</span></div>",
        unsafe_allow_html=True)

# ── Ödül ──────────────────────────────────────────────────────────────────────
if st.session_state.reward:
    st.markdown(
        f'<div class="reward-banner reward-{st.session_state.reward_type}">'
        f'{st.session_state.reward}</div>',
        unsafe_allow_html=True)

# ── Soru Kartı ────────────────────────────────────────────────────────────────
q_text    = q["soru"].replace("<","&lt;").replace(">","&gt;")
donem_lbl = q.get("donem","—")
q_id      = q.get("id", idx+1)

st.markdown(f"""
<div class="q-card">
  <div class="q-tag">MÜLAKAT SORUSU <span class="q-id">#{q_id}</span></div>
  <div class="q-text">{q_text}</div>
  <div class="q-foot">KAYNAK · <span>{donem_lbl}</span></div>
</div>""", unsafe_allow_html=True)


# ── Buton aksiyonları — form yoluyla ─────────────────────────────────────────
# HTML butonlar görsel tarafı hallediyor; Streamlit butonları invisible olarak
# state değişikliğini tetikliyor. Tam uyum için st.form + submit kullanıyoruz.

geri_disabled  = idx == 0
ileri_disabled = (st.session_state.mode == "sıralı" and idx >= len(filtered)-1)
ans_lbl        = "🔒 GİZLE" if st.session_state.show_ans else "🔓 CEVAP"

# HTML buton grid — görsel
st.markdown(f"""
<div class="btn-grid">
  <div class="hbtn {'gray' if geri_disabled else 'blue'}" id="btn-geri"
       style="{'opacity:.25;pointer-events:none' if geri_disabled else ''}">
    ◀ GERİ
  </div>
  <div class="hbtn green" id="btn-cevap">{ans_lbl}</div>
  <div class="hbtn {'gray' if ileri_disabled else 'blue'}" id="btn-ileri"
       style="{'opacity:.25;pointer-events:none' if ileri_disabled else ''}">
    İLERİ ▶
  </div>
  <div class="hbtn orange" id="btn-sans">🎲 ŞANS</div>
</div>""", unsafe_allow_html=True)

# Streamlit butonları — işlevsel (görünmez değil ama küçük, altta)
c1, c2, c3, c4 = st.columns([1, 1.5, 1, 1])
with c1:
    if st.button("◀", disabled=geri_disabled, key="geri"):
        st.session_state.index   -= 1
        st.session_state.show_ans = False
        st.session_state.reward   = ""
        st.rerun()
with c2:
    if st.button(ans_lbl, key="cevap"):
        st.session_state.show_ans = not st.session_state.show_ans
        if st.session_state.show_ans:
            st.session_state.seen += 1
            if st.session_state.seen in REWARDS:
                msg, rtype = REWARDS[st.session_state.seen]
                st.session_state.reward      = msg
                st.session_state.reward_type = rtype
            else:
                st.session_state.reward = ""
        st.rerun()
with c3:
    if st.button("▶", disabled=ileri_disabled, key="ileri"):
        if st.session_state.mode == "rastgele":
            st.session_state.index = random.randint(0, len(filtered)-1)
        elif st.session_state.index < len(filtered)-1:
            st.session_state.index += 1
        st.session_state.show_ans = False
        st.session_state.reward   = ""
        st.rerun()
with c4:
    if st.button("🎲", key="sans"):
        st.session_state.index    = random.randint(0, len(filtered)-1)
        st.session_state.show_ans = False
        st.session_state.reward   = ""
        st.rerun()


# ── Cevap Kartı ───────────────────────────────────────────────────────────────
if st.session_state.show_ans:
    cevap = q.get("cevap","—").replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""
<div class="a-card">
  <div class="a-head">▶ MÜLAKAT CEVABI</div>
  <div class="a-body">{cevap}</div>
</div>""", unsafe_allow_html=True)

    # Google butonu
    google_url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(q["soru"])
    st.markdown(
        f'<a href="{google_url}" target="_blank" style="'
        'display:flex;align-items:center;justify-content:center;gap:8px;'
        'margin-bottom:12px; height:46px; border-radius:8px;'
        'background:#0b0d11; border:1px solid #30363d;'
        'font-family:Rajdhani,sans-serif; font-weight:700;'
        'font-size:13px; letter-spacing:2px; color:#6b7280;'
        'text-decoration:none; text-transform:uppercase;">'
        '🔍 GOOGLE\'DA ARA</a>',
        unsafe_allow_html=True)

# ── Alt ───────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
ci, cr = st.columns([3,1])
with ci:
    st.markdown(
        f"<div style='font-family:Share Tech Mono,monospace;font-size:9px;"
        f"color:#2a3040;letter-spacing:1px;padding-top:10px'>"
        f"POMEM OPS v2.3 · {len(data)} SORU · MUTEDRA POLİCE OLUYOR 🚔</div>",
        unsafe_allow_html=True)
with cr:
    if st.button("↺ SIFIRLA", key="sifirla"):
        st.session_state.index         = 0
        st.session_state.show_ans      = False
        st.session_state.seen          = 0
        st.session_state.filtered_data = get_filtered()
        st.session_state.reward        = ""
        st.rerun()
