import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: rgba(10, 25, 20, 0.98); color: white; }
    .royal-card { background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .stButton>button { background-color: #D4AC0D; color: black; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ربط وجلب كافة كلمات ملف Vocab.csv (1011 كلمة) ---
@st.cache_data
def load_all_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة الملف بالكامل وتجاهل الأخطاء في التنسيق لجلب كل السطور
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        # تنظيف الكلمات من الأرقام والمسافات الزائدة
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Success", "Arabic": "نجاح"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_all_vocab()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 4. نظام الغرف المنفصلة ---

# (1) غرفة الدعاء (البداية)
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر", use_container_width=True):
        st.session_state.page = "hall"; st.rerun()

# (2) القصر الملكي (القائمة)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>تم تحميل {len(st.session_state.db)} كلمة بنجاح ✅</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس والنطق 🔊", use_container_width=True): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار الكلمات (تحقق ✅)", use_container_width=True): st.session_state.page = "test"; st.rerun()
    with col2:
        if st.button("⏳ تحدي الـ 60 ثانية ⚡", use_container_width=True): 
            st.session_state.start_time = time.time(); st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ بناء الجمل", use_container_width=True): st.session_state.page = "sentences"; st.rerun()

# (3) القاموس (يعرض الـ 1011 كلمة كاملة)
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 مكتبة الكلمات الشاملة</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن أي كلمة:")
    for i, w in enumerate(st.session_state.db):
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"v_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['English']}&type=2")

# (4) غرفة الاختبار مع زر "تحقق من الكلمة"
elif st.session_state.page == "test":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    if 'q' not in st.session_state: st.session_state.q = random.choice(st.session_state.db)
    
    st.markdown(f"<div class='royal-card'><h3>ما ترجمة كلمة:</h3><h1 class='gold-text'>{st.session_state.q['English']}</h1></div>", unsafe_allow_html=True)
    
    user_ans = st.text_input("اكتب الترجمة العربية هنا:")
    
    # زر التحقق الأساسي
    if st.button("تحقق من الكلمة ✅", use_container_width=True):
        if user_ans.strip() == st.session_state.q['Arabic']:
            st.success("إجابة صحيحة مئة بالمئة! +10 نقاط")
            st.session_state.score += 10
            st.session_state.q = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"للأسف خطأ! الكلمة الصحيحة هي: {st.session_state.q['Arabic']}")

# (5) تحدي الـ 60 ثانية (مع التحقق الفوري)
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("رجوع", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        ans = st.text_input("الإجابة:", key="bz")
        if st.button("تحقق ✅"):
            if ans.strip() == word['Arabic']:
                st.session_state.score += 50; st.rerun()
            else:
                st.warning("حاول مرة أخرى!")

