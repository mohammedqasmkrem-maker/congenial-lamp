import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية (روح البصرة والجبيلة) ---
st.set_page_config(page_title="Abt Royal Academy - Al-Jubaila", layout="wide")
st.markdown("""
    <style>
    .stApp { background: rgba(10, 25, 20, 0.98); color: white; }
    .royal-card { 
        background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; 
        border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; 
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .stButton>button { 
        background-color: #D4AC0D !important; color: black !important; 
        font-weight: bold !important; border-radius: 10px !important; width: 100%; 
    }
    .jubaila-img { border-radius: 15px; border: 2px solid #D4AC0D; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة بالكامل ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Hello", "Arabic": "مرحباً"}]

# --- 3. تهيئة الذاكرة ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# دالة النطق
def speak(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. غرف الأكاديمية الملكية ---

# (1) غرفة الدعاء (البداية)
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    st.image("[attachment_0](attachment)", caption="تحية لأهل الجبيلة الكرام", use_container_width=True)
    if st.button("آمين - دخول القصر"):
        st.session_state.page = "hall"; st.rerun()

# (2) القصر الرئيسي (القائمة)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي - فرع الجبيلة 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس والنطق الشامل 🔊"): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار التحقق والنطق"): st.session_state.page = "test"; st.rerun()
        if st.button("👤 الملف الشخصي (ابن الجبيلة)"): st.session_state.page = "profile"; st.rerun()
    with col2:
        if st.button("⏳ تحدي 60 ثانية (نطق + تحقق)"): 
            st.session_state.start_time = time.time()
            st.session_state.b_word = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ تكوين الجمل"): st.session_state.page = "sentences"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

# (3) القاموس (النطق لـ 1011 كلمة)
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    search = st.text_input("🔍 ابحث وانطق أي كلمة من ملفك:")
    for i, w in enumerate(st.session_state.db[:150]):
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"spk_{i}"): speak(w['English'])

# (4) الملف الشخصي (صور الجبيلة)
elif st.session_state.page == "profile":
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<div class='royal-card'><h1 class='gold-text'>👤 الملف الشخصي الحقيقي</h1></div>", unsafe_allow_html=True)
    st.image("[attachment_0](attachment)", width=400)
    st.write(f"### النقاط: {st.session_state.score}")
    st.write("### الرتبة: ملك الجبيلة الأبتي 👑")

# (5) تحدي الـ 60 ثانية (نطق + تحقق)
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
        word = st.session_state.b_word
        st.write(f"### الكلمة: {word['English']}")
        if st.button("اسمع النطق 🔊"): speak(word['English'])
        ans = st.text_input("الترجمة:")
        if st.button("تحقق ✅"):
            if ans.strip() == word['Arabic']:
                st.session_state.score += 50
                st.session_state.b_word = random.choice(st.session_state.db)
                st.success("صح! استمر"); time.sleep(0.5); st.rerun()
    
