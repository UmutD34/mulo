import streamlit as st
import json
import random
import time

st.set_page_config(
    page_title="POMEM OPS — Mülakat Simülatörü",
    page_icon="🚔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  CSS — Tactical Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Noto+Sans:wght@300;400;600&display=swap" rel="stylesheet">

<style>
/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    background-color: #0a0c10 !important;
    color: #c9d1d9 !important;
    font-family: 'Noto Sans', sans-serif !important;
}

/* Streamlit container */
.block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 780px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 2px; }

/* ── HUD Header ── */
.hud-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid #21262d;
    border-radius: 12px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hud-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #1f6feb, #58a6ff, #1f6feb);
    background-size: 200% 100%;
    animation: scanline 3s linear infinite;
}
@keyframes scanline {
    0% { background-position: -100% 0; }
    100% { background-position: 200% 0; }
}
.hud-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #58a6ff;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.hud-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #3d444d;
    letter-spacing: 2px;
    margin-top: 2px;
}
.hud-badge {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 6px 14px;
    text-align: center;
}
.badge-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f0883e;
}
.badge-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Progress Bar ── */
.progress-wrap {
    margin-bottom: 20px;
}
.progress-meta {
    display: flex;
    justify-content: space-between;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #6e7681;
    margin-bottom: 6px;
}
.progress-track {
    background: #161b22;
    border-radius: 4px;
    height: 6px;
    border: 1px solid #21262d;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #1f6feb, #58a6ff);
    border-radius: 4px;
    transition: width 0.4s ease;
}

/* ── Mode Selector ── */
.mode-row {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
.mode-btn {
    flex: 1;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
    cursor: pointer;
    font-family: 'Rajdhani', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #6e7681;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.2s;
}
.mode-btn.active {
    background: #1c2128;
    border-color: #58a6ff;
    color: #58a6ff;
    box-shadow: 0 0 12px rgba(88,166,255,0.15);
}

/* ── Soru Kartı ── */
.q-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 30px 28px 26px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.35s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.q-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #58a6ff, #1f6feb);
    border-radius: 4px 0 0 4px;
}
.q-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #3d444d;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.q-id-badge {
    display: inline-block;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 4px;
    padding: 2px 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #58a6ff;
    margin-left: 10px;
}
.q-text {
    font-family: 'Noto Sans', sans-serif;
    font-size: 19px;
    font-weight: 600;
    color: #e6edf3;
    line-height: 1.55;
}
.q-donem {
    margin-top: 16px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #3d444d;
    letter-spacing: 2px;
}
.q-donem span {
    color: #f0883e;
}

/* ── Cevap Kutusu ── */
.a-card {
    background: #0d1117;
    border: 1px solid #238636;
    border-radius: 14px;
    padding: 26px 28px;
    margin-bottom: 18px;
    animation: revealAns 0.4s ease;
    position: relative;
    overflow: hidden;
}
@keyframes revealAns {
    from { opacity: 0; transform: scaleY(0.92); transform-origin: top; }
    to   { opacity: 1; transform: scaleY(1); }
}
.a-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #3fb950, #238636);
    border-radius: 4px 0 0 4px;
}
.a-header {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #3fb950;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.a-header::before {
    content: '▶';
    font-size: 8px;
}
.a-text {
    font-family: 'Noto Sans', sans-serif;
    font-size: 16px;
    color: #b1bac4;
    line-height: 1.75;
    white-space: pre-line;
}

/* ── Streamlit butonları ── */
.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: 10px 0 !important;
    height: 44px !important;
    transition: all 0.2s !important;
    border: 1px solid #30363d !important;
    background: #161b22 !important;
    color: #8b949e !important;
    width: 100% !important;
}
.stButton > button:hover:not(:disabled) {
    background: #1c2128 !important;
    border-color: #58a6ff !important;
    color: #58a6ff !important;
    box-shadow: 0 0 14px rgba(88,166,255,0.15) !important;
}
.stButton > button:disabled {
    opacity: 0.3 !important;
    cursor: not-allowed !important;
}
/* Cevap butonu özel */
div[data-testid="column"]:nth-child(2) .stButton > button {
    border-color: #238636 !important;
    color: #3fb950 !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: #162c20 !important;
    border-color: #3fb950 !important;
    box-shadow: 0 0 14px rgba(63,185,80,0.2) !important;
    color: #56d364 !important;
}
/* Rastgele butonu özel */
div[data-testid="column"]:nth-child(4) .stButton > button {
    border-color: #bb8009 !important;
    color: #f0883e !important;
}
div[data-testid="column"]:nth-child(4) .stButton > button:hover {
    background: #271d0a !important;
    color: #ffa657 !important;
    box-shadow: 0 0 14px rgba(240,136,62,0.2) !important;
}

/* Selectbox & number input */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #0d1117 !important;
    border-color: #30363d !important;
    color: #c9d1d9 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 8px !important;
}
.stSelectbox label, .stNumberInput label, .stSlider label {
    color: #6e7681 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }

/* ── Stat Row ── */
.stat-row {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
.stat-box {
    flex: 1;
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
}
.stat-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 26px;
    font-weight: 700;
    line-height: 1;
}
.stat-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: #6e7681;
    letter-spacing: 1px;
    margin-top: 4px;
    text-transform: uppercase;
}
.streak { color: #f0883e; }
.seen   { color: #58a6ff; }
.total  { color: #3fb950; }

/* ── Separator ── */
hr { border: none; border-top: 1px solid #21262d !important; margin: 20px 0 !important; }

/* ── Jump input ── */
.stNumberInput > div { flex-direction: row !important; align-items: center; }

/* ── Toast / Bildirim ── */
.toast {
    background: #162c20;
    border: 1px solid #238636;
    border-radius: 8px;
    padding: 10px 18px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: #3fb950;
    letter-spacing: 1px;
    text-align: center;
    margin-bottom: 16px;
    animation: fadeUp 0.3s ease;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Veri Yükleme
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        with open("sorular.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            with open("pomem_sorular_unique.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return [{"id": 1, "soru": "sorular.json dosyası bulunamadı.", "cevap": "Dosya yolunu kontrol et.", "donem": "—"}]

data = load_data()
max_index = len(data) - 1

# Dönem listesi
donemler = sorted(set(q.get("donem", "—") for q in data))

# ─────────────────────────────────────────────
#  Session State
# ─────────────────────────────────────────────
defaults = {
    "index": 0,
    "show_ans": False,
    "streak": 0,
    "seen": set(),
    "mode": "sıralı",     # "sıralı" | "rastgele"
    "filter_donem": "Tümü",
    "filtered_data": data,
    "history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  Yardımcı Fonksiyonlar
# ─────────────────────────────────────────────
def get_filtered():
    fd = st.session_state.filter_donem
    if fd == "Tümü":
        return data
    return [q for q in data if q.get("donem", "—") == fd]

def current_item():
    fd = st.session_state.filtered_data
    idx = st.session_state.index
    if not fd:
        return data[0]
    idx = max(0, min(idx, len(fd) - 1))
    return fd[idx]

def go_next():
    fd = st.session_state.filtered_data
    if st.session_state.mode == "rastgele":
        st.session_state.index = random.randint(0, len(fd) - 1)
    else:
        if st.session_state.index < len(fd) - 1:
            st.session_state.index += 1
    st.session_state.show_ans = False

def go_prev():
    if st.session_state.index > 0:
        st.session_state.index -= 1
    st.session_state.show_ans = False

def go_random():
    fd = st.session_state.filtered_data
    st.session_state.index = random.randint(0, len(fd) - 1)
    st.session_state.show_ans = False


# ─────────────────────────────────────────────
#  Filtre değişince sıfırla
# ─────────────────────────────────────────────
def apply_filter():
    st.session_state.filtered_data = get_filtered()
    st.session_state.index = 0
    st.session_state.show_ans = False

filtered = st.session_state.filtered_data
if not filtered:
    filtered = data
    st.session_state.filtered_data = data

q = current_item()
st.session_state.seen.add(q.get("id", st.session_state.index))


# ─────────────────────────────────────────────
#  UI — HUD Header
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hud-header">
    <div>
        <div class="hud-title">🚔 POMEM OPS</div>
        <div class="hud-subtitle">MÜLAKAT SİMÜLATÖRÜ · AKTİF</div>
    </div>
    <div class="hud-badge">
        <div class="badge-val">{len(filtered)}</div>
        <div class="badge-lbl">SORU</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Stat Row
# ─────────────────────────────────────────────
streak_fire = "🔥" if st.session_state.streak >= 5 else ("⚡" if st.session_state.streak >= 2 else "")
st.markdown(f"""
<div class="stat-row">
    <div class="stat-box">
        <div class="stat-val streak">{st.session_state.streak} {streak_fire}</div>
        <div class="stat-lbl">Seri</div>
    </div>
    <div class="stat-box">
        <div class="stat-val seen">{len(st.session_state.seen)}</div>
        <div class="stat-lbl">Görülen</div>
    </div>
    <div class="stat-box">
        <div class="stat-val total">{len(data)}</div>
        <div class="stat-lbl">Toplam</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Progress Bar
# ─────────────────────────────────────────────
pct = round((st.session_state.index + 1) / len(filtered) * 100, 1)
st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-meta">
        <span>İLERLEME</span>
        <span>{st.session_state.index + 1} / {len(filtered)} — %{pct}</span>
    </div>
    <div class="progress-track">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Filtreler (sidebar benzeri, gizli expander)
# ─────────────────────────────────────────────
with st.expander("⚙️  FİLTRELER & AYARLAR", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        new_donem = st.selectbox(
            "DÖNEM FİLTRESİ",
            ["Tümü"] + donemler,
            index=(["Tümü"] + donemler).index(st.session_state.filter_donem)
        )
        if new_donem != st.session_state.filter_donem:
            st.session_state.filter_donem = new_donem
            apply_filter()
            st.rerun()
    with col_b:
        jump = st.number_input(
            "SORU NUMARASINA ATLA",
            min_value=1,
            max_value=len(filtered),
            value=st.session_state.index + 1,
            step=1
        )
        if st.button("🎯  ATLA", use_container_width=True):
            st.session_state.index = jump - 1
            st.session_state.show_ans = False
            st.rerun()


# ─────────────────────────────────────────────
#  Soru Kartı
# ─────────────────────────────────────────────
donem_label = q.get("donem", "—")
q_id = q.get("id", st.session_state.index + 1)

st.markdown(f"""
<div class="q-card">
    <div class="q-tag">MÜLAKAT SORUSU <span class="q-id-badge">#{q_id}</span></div>
    <div class="q-text">{q['soru']}</div>
    <div class="q-donem">KAYNAK · <span>{donem_label}</span></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Kontrol Butonları
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([1, 1.4, 1, 1])

with c1:
    if st.button("◀  GERİ", disabled=(st.session_state.index == 0)):
        go_prev()
        st.rerun()

with c2:
    ans_label = "🔒  CEVABI GİZLE" if st.session_state.show_ans else "🔓  CEVABI GÖR"
    if st.button(ans_label, use_container_width=True):
        st.session_state.show_ans = not st.session_state.show_ans
        if st.session_state.show_ans:
            st.session_state.streak += 1
        st.rerun()

with c3:
    if st.button("İLERİ  ▶", disabled=(st.session_state.mode == "sıralı" and st.session_state.index >= len(filtered) - 1)):
        go_next()
        st.rerun()

with c4:
    if st.button("🎲  ŞANS", use_container_width=True):
        go_random()
        st.session_state.streak = 0
        st.rerun()


# ─────────────────────────────────────────────
#  Mod Seçimi (küçük toggle)
# ─────────────────────────────────────────────
st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
col_m1, col_m2, col_m3 = st.columns([1, 1, 2])
with col_m1:
    if st.button("📋  SIRALI MOD", use_container_width=True):
        st.session_state.mode = "sıralı"
        st.rerun()
with col_m2:
    if st.button("🔀  RASTGELE MOD", use_container_width=True):
        st.session_state.mode = "rastgele"
        st.rerun()
with col_m3:
    mode_display = "SIRALI" if st.session_state.mode == "sıralı" else "RASTGELE"
    st.markdown(f"""
    <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#6e7681;
         padding:12px 0; letter-spacing:2px; text-align:right;">
        AKTİF MOD · <span style="color:#58a6ff">{mode_display}</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Cevap Kutusu
# ─────────────────────────────────────────────
if st.session_state.show_ans:
    cevap_text = q.get("cevap", "—").replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f"""
<div class="a-card">
    <div class="a-header">MÜLAKAT CEVABI</div>
    <div class="a-text">{cevap_text}</div>
</div>
""", unsafe_allow_html=True)

    # Seri tebrik mesajı
    if st.session_state.streak > 0 and st.session_state.streak % 5 == 0:
        st.markdown(f"""
<div class="toast">
    🔥 {st.session_state.streak} SORU SERISI — YANMAYA DEVAM EDİYORSUN!
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Sıfırlama
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
col_r1, col_r2 = st.columns([3, 1])
with col_r2:
    if st.button("↺  SIFIRLA", use_container_width=True):
        st.session_state.index = 0
        st.session_state.show_ans = False
        st.session_state.streak = 0
        st.session_state.seen = set()
        st.session_state.filtered_data = get_filtered()
        st.rerun()
with col_r1:
    st.markdown(f"""
    <div style="font-family:'Share Tech Mono',monospace; font-size:10px; color:#3d444d;
         padding-top:12px; letter-spacing:1px;">
        POMEM OPS v2.0 · {len(data)} SORU YÜKLENDİ · MUTEDRA POLİCE OLUYOR 🚔
    </div>
    """, unsafe_allow_html=True)
