import streamlit as st
import json

# Sayfa Genişlik ve Başlık Ayarları
st.set_page_config(
    page_title="POMEM Mülakat Kartları",
    page_icon="👮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Tasarımı
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .card-box { background-color: #ffffff; padding: 35px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-left: 6px solid #1E3A8A; margin-top: 20px; margin-bottom: 20px; }
    .question-title { font-size: 14px; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .question-text { font-size: 22px; font-weight: 700; color: #1F2937; line-height: 1.4; }
    .answer-box { background-color: #F0F4F8; padding: 25px; border-radius: 12px; border-top: 3px solid #10B981; margin-top: 20px; font-size: 18px; color: #374151; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        with open("sorular.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return [{"id": 1, "soru": "Veri dosyası (sorular.json) bulunamadı.", "cevap": "Dizini kontrol edin."}]

data = load_data()
max_index = len(data) - 1

# Hafıza Alanı (Session State) Tanımlamaları
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.show_ans = False

current_item = data[st.session_state.current_index]

st.title("MUTEDRA POLİCE OLUYOR KRALLLLLLLLLLLIMMM")
st.caption(f"Soru: {st.session_state.current_index + 1} / {len(data)}")

st.markdown(f"""
    <div class="card-box">
        <div class="question-title">SORU #{current_item.get('id', st.session_state.current_index + 1)}</div>
        <div class="question-text">{current_item['soru']}</div>
    </div>
""", unsafe_allow_html=True)

# Buton Alanları (İleri, Geri, Cevap)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️ Geri", use_container_width=True, disabled=(st.session_state.current_index == 0)):
        st.session_state.current_index -= 1
        st.session_state.show_ans = False
        st.rerun()

with col2:
    if st.button("👁️ Cevap", use_container_width=True):
        st.session_state.show_ans = not st.session_state.show_ans

with col3:
    if st.button("İleri ➡️", use_container_width=True, disabled=(st.session_state.current_index == max_index)):
        st.session_state.current_index += 1
        st.session_state.show_ans = False
        st.rerun()

# Cevap Alanı
if st.session_state.show_ans:
    st.markdown(f"""
        <div class="answer-box">
            <strong>Mülakat Yanıtı:</strong><br><br>
            {current_item['cevap']}
        </div>
    """, unsafe_allow_html=True)
