import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية والفخامة ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.96); z-index: -1; }
    .royal-card { background: rgba(20, 35, 30, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px; color: white; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. جلب البيانات من ملفك vocab.csv ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv" #
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True) #
        return df.dropna().to_dict('records')
    except: return [{"English": "Time", "Arabic": "الوقت"}]

# --- 3. تهيئة الذاكرة (منع الأخطاء) ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'page' not in st.session_state: st.session_state.page = "dua" # يبدأ بالدعاء حتماً
if 'score' not in st.session_state: st.session_state.score = 0

# --- 4. نظام الغرف المنفصلة ---

# غرفة (1): الدعاء عند الدخول
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول الأكاديمية", use_container_width=True):
        st.session_state.page = "hall"
        st.rerun()

# غرفة (2): القاعة الرئيسية (القصر)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:white;'>إجمالي نقاطك الملكية: {st.session_state.score}</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>📖 القاموس</h2><p>استعراض الـ 1011 كلمة</p></div>", unsafe_allow_html=True)
        if st.button("فتح المكتبة 📚", use_container_width=True): st.session_state.page = "dictionary"

        st.markdown("<div class='royal-card'><h2 class='gold-text'>✍️ اختبار كلمات</h2><p>بدون وقت (ترجمة)</p></div>", unsafe_allow_html=True)
        if st.button("بدء الاختبار ⚔️", use_container_width=True): st.session_state.page = "normal_test"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>⏳ تحدي الذكاء</h2><p>60 ثانية ضد الوقت</p></div>", unsafe_allow_html=True)
        if st.button("ابدأ تحدي الـ 60 ثانية ⚡", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.page = "blitz_test"

        st.markdown("<div class='royal-card'><h2 class='gold-text'>🛠️ تكوين جمل</h2><p>أكمل الفراغ بالإنجليزية</p></div>", unsafe_allow_html=True)
        if st.button("بناء الجمل الملكية 🔨", use_container_width=True): st.session_state.page = "sentence_build"

# غرفة (3): القاموس (بحث فقط)
elif st.session_state.page == "dictionary":
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 قاموس الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن كلمة إنجليزية أو عربية:")
    for w in st.session_state.db:
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            st.write(f"**{w['English']}** : {w['Arabic']}")

# غرفة (4): اختبار الكلمات العادي (بدون وقت)
elif st.session_state.page == "normal_test":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    if 'current_w' not in st.session_state: st.session_state.current_w = random.choice(st.session_state.db)
    word = st.session_state.current_w
    st.markdown(f"<div class='royal-card'><h2 class='gold-text'>{word['English']}</h2><p>ما ترجمة هذه الكلمة بالعربي؟</p></div>", unsafe_allow_html=True)
    ans = st.text_input("الإجابة:")
    if st.button("تحقق"):
        if ans == word['Arabic']:
            st.success("إجابة صحيحة! +10 نقاط")
            st.session_state.score += 10
            st.session_state.current_w = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()

# غرفة (5): تحدي الـ 60 ثانية (الذكاء الاصطناعي)
elif st.session_state.page == "blitz_test":
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    if remaining <= 0:
        st.error("💥 انتهى الوقت!")
        if st.button("العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    else:
        st.markdown(f"<h2 style='color:red; text-align:center;'>⏳ {remaining} ثانية</h2>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("اكتب بسرعة:", key="blitz").strip() == word['Arabic']:
            st.session_state.score += 60 # نقاط عالية للسرعة
            st.rerun()

# غرفة (6): تكوين الجمل (أكمل الفراغ)
elif st.session_state.page == "sentence_build":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>The __ is very helpful here.</h3><p>(المطلوب كلمة: {word['Arabic']})</p></div>", unsafe_allow_html=True)
    ans = st.text_input("اكتب الكلمة بالإنجليزية لتكمل الجملة:")
    if st.button("بناء ✅"):
        if ans.lower() == word['English'].lower():
            st.success("بناء ملكي صحيح!")
            time.sleep(1); st.rerun()
    
