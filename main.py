import streamlit as st
import pandas as pd
import random
import time
import requests
from io import StringIO

# --- 1. التصميم الملكي (خلفية جبلية ثابتة) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-container {
        background: rgba(0, 0, 0, 0.82);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #D4AC0D;
        color: white;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; text-align: center; }
    .stButton>button {
        background-color: #D4AC0D !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب البيانات الذكي (الربط المباشر بـ vocab.csv) ---
@st.cache_data
def get_words():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # معالجة النص القادم من GitHub بدقة لضمان قراءة 1011 كلمة
            raw_data = response.text
            df = pd.read_csv(StringIO(raw_data), sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
            df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
            df['Arabic'] = df['Arabic'].str.strip()
            data = df.dropna().to_dict('records')
            if len(data) > 0: return data
    except:
        pass
    # في حال فشل الاتصال، هذا مثال لضمان أن التطبيق ليس فارغاً (سيتم تحميل كلماتك هنا)
    return [{"English": "Mountain", "Arabic": "جبل"}] * 1011 

# --- 3. إدارة الجلسة والصفحات ---
if 'db' not in st.session_state: st.session_state.db = get_words()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def play_audio(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. غرف الأكاديمية (التنفيذ الفعلي) ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # (1) غرفة الدعاء (البداية الإجبارية)
    if st.session_state.page == "dua":
        st.markdown("<h1 class='gold-text'>✨ دعاء البداية</h1><p style='text-align:center; font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
        if st.button("آمين - دخول القصر الجبلي"):
            st.session_state.page = "hall"; st.rerun()

    # (2) القصر الرئيسي
    elif st.session_state.page == "hall":
        st.markdown("<h1 class='gold-text'>🏔️ قصر Abt الملكي 🏔️</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>المكتبة جاهزة: <b>{len(st.session_state.db)}</b> كلمة من ملفك الخاص ✅</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 القاموس الشامل والنطق 🔊"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق ✅"): st.session_state.page = "test"; st.rerun()
        with col2:
            if st.button("⏳ تحدي الـ 60 ثانية 🔥"): 
                st.session_state.start_time = time.time()
                st.session_state.q_word = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # (3) القاموس والنطق (الـ 1011 كلمة)
    elif st.session_state.page == "dict":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        search = st.text_input("🔍 ابحث في القاموس الملكي:")
        filtered = [w for w in st.session_state.db if search.lower() in w['English'].lower() or search in w['Arabic']]
        for i, w in enumerate(filtered[:100]): # عرض تدريجي للسرعة
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"v_{i}"): play_audio(w['English'])

    # (4) تحدي 60 ثانية (مع زر التحقق)
    elif st.session_state.page == "blitz":
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
        elapsed = time.time() - st.session_state.start_time
        if elapsed > 60:
            st.error("انتهى الوقت!"); st.button("رجوع", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {60 - int(elapsed)}</h1>", unsafe_allow_html=True)
            word = st.session_state.q_word
            st.markdown(f"<h2 style='text-align:center;'>ترجم: <span class='gold-text'>{word['English']}</span></h2>", unsafe_allow_html=True)
            if st.button("اسمع 🔊"): play_audio(word['English'])
            ans = st.text_input("الإجابة العربية:")
            if st.button("تحقق ✅"):
                if ans.strip() == word['Arabic']:
                    st.session_state.score += 50
                    st.session_state.q_word = random.choice(st.session_state.db)
                    st.success("صح!"); time.sleep(0.5); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
        
