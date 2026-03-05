import streamlit as st
import pandas as pd
import random
import time

# --- 1. تصميم الواجهة بالذكاء الاصطناعي (خلفية كاملة + ستايل ملكي) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    /* جعل صورة الجبيلة خلفية كاملة للتطبيق */
    .stApp {
        background: url("https://images.unsplash.com/photo-1545562083-a600704fa487?q=80&w=2000");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* حاوية شفافة تجعل النصوص واضحة جداً */
    .main-container {
        background: rgba(0, 0, 0, 0.85);
        padding: 40px;
        border-radius: 25px;
        border: 3px solid #D4AC0D;
        margin: 20px;
    }
    
    .royal-card {
        background: rgba(40, 60, 50, 0.9);
        border: 2px solid #D4AC0D;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .gold-text { color: #D4AC0D !important; font-weight: bold; text-shadow: 2px 2px 4px #000; }
    
    /* ستايل أزرار التحقق الملكية */
    .stButton>button {
        background-color: #D4AC0D !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #F1C40F !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة كاملة (بدون نقصان) ---
@st.cache_data
def load_all_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة كل السطور (on_bad_lines تجاهل الأخطاء البسيطة لضمان جلب كل الكلمات)
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        # تحويلها لقائمة كاملة (المفروض تطلع 1011 كلمة)
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Welcome", "Arabic": "أهلاً بك"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_all_vocab()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def speak(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. غرف التطبيق المنظمة ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # (غرفة 1) الدعاء والترحيب
    if st.session_state.page == "dua":
        st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
        if st.button("آمين - دخول قصر الجبيلة"):
            st.session_state.page = "hall"; st.rerun()

    # (غرفة 2) القصر الرئيسي
    elif st.session_state.page == "hall":
        st.markdown(f"<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
        st.write(f"<p style='text-align:center; color:white;'>تم تحميل القاموس الملكي: {len(st.session_state.db)} كلمة جاهزة</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 القاموس والنطق الشامل 🔊"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق (بدون وقت)"): st.session_state.page = "test"; st.rerun()
            if st.button("👤 الملف الشخصي الحقيقي"): st.session_state.page = "profile"; st.rerun()
        with col2:
            if st.button("⏳ تحدي الـ 60 ثانية (تحقق)"): 
                st.session_state.start_time = time.time()
                st.session_state.b_word = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("🛠️ تكوين وبناء الجمل"): st.session_state.page = "sentences"; st.rerun()
            if st.button("🌿 غرفة الاسترخاء الطبيعية"): st.session_state.page = "relax"; st.rerun()

    # (غرفة 3) القاموس (كل الـ 1011 كلمة هنا)
    elif st.session_state.page == "dict":
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        st.markdown("<h2 class='gold-text'>📖 مكتبة الـ 1011 كلمة كاملة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في القاموس:")
        # تم ضبطه ليعرض كل الكلمات بناءً على البحث
        count = 0
        for i, w in enumerate(st.session_state.db):
            if search.lower() in w['English'].lower() or search in w['Arabic']:
                if count < 100: # نعرض 100 كلمة بالمرة الواحدة لسرعة التطبيق
                    c1, c2 = st.columns([5, 1])
                    c1.write(f"**{w['English']}** = {w['Arabic']}")
                    if c2.button("🔊", key=f"d_{i}"): speak(w['English'])
                    count += 1

    # (غرفة 4) تحدي الـ 60 ثانية (مع زر التحقق)
    elif st.session_state.page == "blitz":
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
        rem = 60 - int(time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            word = st.session_state.b_word
            st.markdown(f"<div class='royal-card'><h3>ترجم بسرعة: <b class='gold-text'>{word['English']}</b></h3></div>", unsafe_allow_html=True)
            if st.button("اسمع الكلمة 🔊"): speak(word['English'])
            ans = st.text_input("أدخل الترجمة العربية:")
            if st.button("تحقق من الكلمة ✅"):
                if ans.strip() == word['Arabic']:
                    st.session_state.score += 50
                    st.session_state.b_word = random.choice(st.session_state.db)
                    st.success("أحسنت! +50 نقطة")
                    time.sleep(0.5); st.rerun()
                else:
                    st.error("خطأ! حاول مرة ثانية")

    st.markdown('</div>', unsafe_allow_html=True)
    
