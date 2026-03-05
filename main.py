import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.98); z-index: -1; }
    .royal-card { background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; color: white; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .back-btn { background-color: #D4AC0D; color: black !important; font-weight: bold; border-radius: 10px; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.dropna().to_dict('records')
    except: return [{"English": "Success", "Arabic": "نجاح"}]

if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 3. نظام التنقل والغرف ---

# غرفة (1): الدعاء
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر", use_container_width=True):
        st.session_state.page = "hall"; st.rerun()

# غرفة (2): القصر الرئيسي
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 الملف الشخصي", use_container_width=True): st.session_state.page = "profile"; st.rerun()
        if st.button("📚 القاموس والتحقق", use_container_width=True): st.session_state.page = "dict"; st.rerun()
    with col2:
        if st.button("⏳ تحدي الـ 60 ثانية", use_container_width=True): st.session_state.start_time = time.time(); st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ بناء الجمل", use_container_width=True): st.session_state.page = "sentences"; st.rerun()
    if st.button("🌿 غرفة الاسترخاء", use_container_width=True): st.session_state.page = "relax"; st.rerun()

# غرفة (3): القاموس مع نظام التحقق
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر الرئيسي", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 القاموس واختبار الحفظ</h2>", unsafe_allow_html=True)
    
    word_to_test = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>اختبر نفسك: كيف تترجم ({word_to_test['English']})؟</h3></div>", unsafe_allow_html=True)
    user_trans = st.text_input("اكتب الترجمة العربية هنا:")
    if st.button("تحقق من الترجمة ✅"):
        if user_trans.strip() == word_to_test['Arabic']:
            st.success("إجابة صحيحة! بطل")
        else:
            st.error(f"خطأ! الترجمة الصحيحة هي: {word_to_test['Arabic']}")
    
    st.divider()
    search = st.text_input("🔍 أو ابحث عن كلمة في القاموس:")
    for w in st.session_state.db[:50]: # عرض عينة للسرعة
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            st.write(f"**{w['English']}** = {w['Arabic']}")

# غرفة (4): الملف الشخصي
elif st.session_state.page == "profile":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.markdown(f"<div class='royal-card'><h1>👤 ملفك الحقيقي</h1><h2>نقاطك: {st.session_state.score}</h2></div>", unsafe_allow_html=True)

# غرفة (5): تحدي الـ 60 ثانية
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h2 style='color:red;'>⏳ {rem} ثانية</h2>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم: **{word['English']}**")
        if st.text_input("الإجابة:", key="speed").strip() == word['Arabic']:
            st.session_state.score += 60; st.rerun()

# غرفة (6): غرفة الاسترخاء
elif st.session_state.page == "relax":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    
