import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import io

# إعدادات الصفحة والألوان
st.set_page_config(page_title="تحدي الألف كلمة", page_icon="🎓")

# تنسيق الأزرار والألوان باستخدام CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #f0f2f6;
        color: #1f77b4;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        height: 3em;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1f77b4;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('vocab.csv')

df = load_data()

# تهيئة عداد النقاط والكلمة
if 'score' not in st.session_state: st.session_state.score = 0
if 'count' not in st.session_state: st.session_state.count = 0

if 'current_word' not in st.session_state:
    st.session_state.current_word = df.sample(n=1).iloc[0]
    correct = st.session_state.current_word['Arabic Translation']
    wrong = df[df['Arabic Translation'] != correct]['Arabic Translation'].sample(n=3).tolist()
    options = wrong + [correct]
    random.shuffle(options)
    st.session_state.options = options

word_info = st.session_state.current_word

# واجهة التطبيق
st.title("📖 تطبيق الـ 1000 كلمة")
st.write(f"⭐ النقاط: {st.session_state.score} | 🔄 الكلمات المراجعة: {st.session_state.count}")
st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"ما معنى كلمة:  **{word_info['English Word']}** ؟")
with col2:
    # إضافة زر النطق
    tts = gTTS(text=word_info['English Word'], lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp, format='audio/mp3')

# عرض الخيارات
for option in st.session_state.options:
    if st.button(option, use_container_width=True):
        if option == word_info['Arabic Translation']:
            st.success("أحسنت! إجابة صحيحة ✅")
            st.session_state.score += 1
        else:
            st.error(f"للأسف خطأ ❌ المعنى هو: {word_info['Arabic Translation']}")
        
        st.session_state.count += 1
        if st.button("الكلمة التالية ➡️"):
            for key in ['current_word', 'options']: del st.session_state[key]
            st.rerun()
          
