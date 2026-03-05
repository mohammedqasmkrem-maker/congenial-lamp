import streamlit as st
import pandas as pd
import random
import time

# --- 1. التصميم الجبلي الملكي (خلفية جبال كاملة) ---
st.set_page_config(page_title="Abt Royal Academy - Mountain Edition", layout="wide")

st.markdown("""
    <style>
    /* خلفية جبلية كاملة للتطبيق */
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* حاوية المحتوى الشفافة */
    .main-container {
        background: rgba(10, 20, 15, 0.85);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #D4AC0D;
        margin: 10px;
        color: white;
    }
    
    .gold-text { color: #D4AC0D !important; font-weight: bold; text-align: center; }
    
    /* أزرار التحقق الملكية */
    .stButton>button {
        background-color: #D4AC0D !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة (الربط الحقيقي بملفك) ---
@st.cache_data
def load_full_data():
    # الرابط المباشر لملفك vocab.csv
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة الملف بالكامل (تجاهل الأخطاء لضمان جلب كل السطور)
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        # تنظيف النصوص
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        # إرجاع كافة الكلمات (1011 كلمة)
        return df.dropna().to_dict('records')
    except Exception as e:
        return [{"English": "Connect File", "Arabic": "اربط الملف"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_full_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def speak(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. غرف الأكاديمية ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # (1) غرفة الدعاء
    if st.session_state.page == "dua":
        st.markdown("<h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='text-align:center; font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
        if st.button("آمين - دخول القصر الجبلي"):
            st.session_state.page = "hall"; st.rerun()

    # (2) القصر الرئيسي
    elif st.session_state.page == "hall":
        st.markdown("<h1 class='gold-text'>🏔️ قصر Abt الجبلي 🏔️</h1>", unsafe_allow_html=True)
        st.write(f"<p style='text-align:center;'>تم ربط القاموس بنجاح: {len(st.session_state.db)} كلمة</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 القاموس والنطق (1011 كلمة)"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق ✅"): st.session_state.page = "test"; st.rerun()
        with col2:
            if st.button("⏳ تحدي الـ 60 ثانية 🔥"): 
                st.session_state.start_time = time.time()
                st.session_state.b_word = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()

    # (3) القاموس الشامل (يعرض كل كلماتك مع نطق)
    elif st.session_state.page == "dict":
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        st.markdown("<h2 class='gold-text'>📖 مكتبة الكلمات الكاملة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في الـ 1011 كلمة:")
        # فلترة وعرض الكلمات
        filtered = [w for w in st.session_state.db if search.lower() in w['English'].lower() or search in w['Arabic']]
        for i, w in enumerate(filtered[:100]): # نعرض 100 لكل عملية بحث للسرعة
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"d_{i}"): speak(w['English'])

    # (4) تحدي 60 ثانية (تحقق + نطق)
    elif st.session_state.page == "blitz":
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
        rem = 60 - int(time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("رجوع", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            word = st.session_state.b_word
            st.markdown(f"<h2 style='text-align:center;'>ترجم: <span class='gold-text'>{word['English']}</span></h2>", unsafe_allow_html=True)
            if st.button("اسمع النطق 🔊"): speak(word['English'])
            ans = st.text_input("اكتب الترجمة العربية:")
            if st.button("تحقق من الكلمة ✅"):
                if ans.strip() == word['Arabic']:
                    st.session_state.score += 50
                    st.session_state.b_word = random.choice(st.session_state.db)
                    st.success("صح! استمر")
                    time.sleep(0.5); st.rerun()
                else:
                    st.error("خطأ! حاول مرة ثانية")

    st.markdown('</div>', unsafe_allow_html=True)
        
