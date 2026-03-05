import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .royal-card { 
        background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; 
        border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; 
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; font-size: 24px; }
    .stButton>button { 
        background-color: #D4AC0D !important; color: black !important; 
        font-weight: bold !important; border-radius: 10px !important; width: 100%; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (قراءة ملف vocab.csv بالكامل) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة الملف ومعالجة الأخطاء لضمان جلب الـ 1011 كلمة
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Welcome", "Arabic": "أهلاً بك"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# دالة النطق الصوتي المباشر
def speak_now(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. غرف الأكاديمية (نظام التنقل) ---

# (1) غرفة الدعاء (البداية)
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    # صورة تعبيرية للمكان (الجبيلة)
    st.image("https://images.unsplash.com/photo-1545562083-a600704fa487?q=80&w=1000", caption="أكاديمية أبت - فرع الجبيلة", use_container_width=True)
    if st.button("آمين - دخول القصر الملكي"):
        st.session_state.page = "hall"
        st.rerun()

# (2) القصر الرئيسي (لوحة التحكم)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    st.write(f"<p style='text-align:center;'>المكتبة جاهزة: {len(st.session_state.db)} كلمة</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس والنطق (الكامل)"): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار التحقق والنطق"): st.session_state.page = "test"; st.rerun()
        if st.button("👤 الملف الشخصي (ابن الجبيلة)"): st.session_state.page = "profile"; st.rerun()
    with col2:
        if st.button("⏳ تحدي 60 ثانية (تحقق + نطق)"): 
            st.session_state.start_time = time.time()
            st.session_state.b_word = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ تكوين الجمل الذكي"): st.session_state.page = "sentences"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

# (3) القاموس والنطق
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 مكتبة الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن كلمة واسمع نطقها:")
    for i, w in enumerate(st.session_state.db[:150]): # عرض عينة كبيرة
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"sp_{i}"): speak_now(w['English'])

# (4) تحدي 60 ثانية (مع زر التحقق والنطق)
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
    rem = 60 - int(time.time() - st.session_state.start_time)
    
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("عودة للقصر", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<div class='royal-card'><h1 style='color:red;'>⏳ {rem} ثانية</h1></div>", unsafe_allow_html=True)
        word = st.session_state.b_word
        st.write(f"### الكلمة: {word['English']}")
        if st.button("اسمع النطق 🔊"): speak_now(word['English'])
        
        ans = st.text_input("اكتب الترجمة العربية:")
        if st.button("تحقق من الكلمة ✅"):
            if ans.strip() == word['Arabic']:
                st.session_state.score += 50
                st.session_state.b_word = random.choice(st.session_state.db)
                st.success("إجابة صحيحة! استمر")
                time.sleep(0.5); st.rerun()
            else:
                st.error("خطأ! حاول مرة أخرى")

# (5) غرفة الاسترخاء
elif st.session_state.page == "relax":
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")

# (6) الملف الشخصي
elif st.session_state.page == "profile":
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown(f"<div class='royal-card'><h1>👤 ملك الجبيلة</h1><h2>نقاطك: {st.session_state.score}</h2></div>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1580674684081-7617fbf3d745?q=80&w=1000", caption="الجبيلة في القلب")
