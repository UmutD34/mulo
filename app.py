import streamlit as st
import json
import random

# Sayfa Genişlik ve Başlık Ayarları
st.set_page_config(
    page_title="POMEM Mülakat Kartları",
    page_icon="👮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Arayüzü Özelleştirmek İçin Gelişmiş CSS Tasarımı
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
    }
    .card-box {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-left: 6px solid #1E3A8A;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .question-title {
        font-size: 14px;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .question-text {
        font-size: 22px;
        font-weight: 700;
        color: #1F2937;
        line-height: 1.4;
    }
    .answer-box {
        background-color: #F0F4F8;
        padding: 25px;
        border-radius: 12px;
        border-top: 3px solid #10B981;
        margin-top: 20px;
        font-size: 18px;
        color: #374151;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# JSON Verisini Yükleme Fonksiyonu
@st.cache_data
def load_data():
    try:
        with open("sorular.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Dosya bulunamazsa test amaçlı dummy veri
        return [
            {"id": 1, "soru": "Veri dosyası (sorular.json) bulunamadı. Lütfen adımları kontrol edin.", "cevap": "Dizini kontrol edin."}
        ]

data = load_data()

# Hafıza Alanı (Session State) Tanımlamaları
if "current_item" not in st.session_state:
    st.session_state.current_item = random.choice(data)
    st.session_state.show_ans = False

# Başlık Bölümü
st.title("👮 POMEM Mülakat Hazırlık")
st.caption(f"Toplam Yüklü Soru Sayısı: {len(data)} | Mobil Uyumlu Dijital Kartlar")

# Soru Kartı Tasarımı (HTML/CSS)
st.markdown(f"""
    <div class="card-box">
        <div class="question-title">SORU #{st.session_state.current_item['id']}</div>
        <div class="question-text">{st.session_state.current_item['soru']}</div>
    </div>
""", unsafe_allow_html=True)

# Buton Alanları
col1, col2 = st.columns(2)

with col1:
    if st.button("👁️ Cevabı Göster / Gizle", use_container_width=True):
        st.session_state.show_ans = not st.session_state.show_ans

with col2:
    if st.button("➡️ Sonraki Rastgele Soru", use_container_width=True):
        st.session_state.current_item = random.choice(data)
        st.session_state.show_ans = False
        st.rerun()

# Cevap Alanı Görünürlük Kontrolü
if st.session_state.show_ans:
    st.markdown(f"""
        <div class="answer-box">
            <strong>Mülakat Yanıtı:</strong><br><br>
            {st.session_state.current_item['cevap']}
        </div>
    """, unsafe_allow_html=True)