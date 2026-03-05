import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية (خلفية الجبيلة الكاملة) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

# هنا نضع صورة الجبيلة كخلفية ثابتة للتطبيق بالكامل
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1545562083-a600704fa487?q=80&w=2000");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* طبقة شفافة لجعل النص واضحاً فوق الخلفية */
    .main-container {
        background: rgba(0, 0, 0, 0.85);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #D4AC0D;
    }
    .royal-card {
        background: rgba(25, 40, 35, 0.9);
        border: 1px solid #D4AC0D;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .stButton>button {
        background-color: #D4AC0D !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (الربط بملف vocab.csv) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Success", "Arabic": "نجاح"}]

if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def speak(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 3. نظام الغرف داخل حاوية شفافة ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # (1) غرفة الدعاء
    if st.session_state.page == "dua":
        st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
        if st.button("آمين - دخول القصر الملكي بالجبيلة"):
            st.session_state.page = "hall"; st.rerun()

    # (2) القصر الرئيسي
    elif st.session_state.page == "hall":
        st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي - الجبيلة 🌲</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 القاموس والنطق 🔊"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        with col2:
            if st.button("⏳ تحدي الـ 60 ثانية ⚡"): 
                st.session_state.start_time = time.time()
                st.session_state.b_word = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("🛠️ تكوين الجمل"): st.session_state.page = "sentences"; st.rerun()
            if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # (3) القاموس والنطق
    elif st.session_state.page == "dict":
        if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
        st.markdown("<h2 class='gold-text'>📖 مكتبة الـ 1011 كلمة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث وانطق:")
        for i, w in enumerate(st.session_state.db[:100]):
            if search.lower() in w['English'].lower() or search in w['Arabic']:
                c1, c2 = st.columns([5, 1])
                c1.write(f"**{w['English']}** = {w['Arabic']}")
                if c2.button("🔊", key=f"s_{i}"): speak(w['English'])

    # (4) تحدي 60 ثانية (تحقق + نطق)
    elif st.session_state.page == "blitz":
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
        rem = 60 - int(time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            word = st.session_state.b_word
            st.write(f"### ترجم: {word['English']}")
            if st.button("اسمع 🔊"): speak(word['English'])
            ans = st.text_input("الترجمة:")
            if st.button("تحقق ✅"):
                if ans.strip() == word['Arabic']:
                    st.session_state.score += 50
                    st.session_state.b_word = random.choice(st.session_state.db)
                    st.success("صح!"); time.sleep(0.5); st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
        
