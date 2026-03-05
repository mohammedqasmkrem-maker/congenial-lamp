import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية والفخامة ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 25, 20, 0.98); z-index: -1;
    }
    .royal-card {
        background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D;
        border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; color: white;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (vocab.csv) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Success", "Arabic": "نجاح"}]

# --- 3. تهيئة النظام والملف الشخصي ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 4. نظام الغرف الملكية ---

# الغرفة (1): الدعاء
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر الملكي", use_container_width=True):
        st.session_state.page = "hall"
        st.rerun()

# الغرفة (2): القاعة الرئيسية
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='royal-card'><h3>👤 الملف الشخصي</h3><p>عرض رتبتك ونقاطك</p></div>", unsafe_allow_html=True)
        if st.button("دخل ملفي الشخصي", use_container_width=True): st.session_state.page = "profile"

        st.markdown("<div class='royal-card'><h3>📖 القاموس الشامل</h3><p>تصفح كلمات ملف vocab.csv</p></div>", unsafe_allow_html=True)
        if st.button("فتح المكتبة 📚", use_container_width=True): st.session_state.page = "dictionary"

        st.markdown("<div class='royal-card'><h3>🌿 غرفة الاسترخاء</h3><p>طبيعة وهدوء</p></div>", unsafe_allow_html=True)
        if st.button("دخول الاسترخاء", use_container_width=True): st.session_state.page = "relax"

    with col2:
        st.markdown("<div class='royal-card'><h3>⏳ تحدي 60 ثانية</h3><p>ذكاء اصطناعي ضد الوقت</p></div>", unsafe_allow_html=True)
        if st.button("ابدأ التحدي السريع", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.page = "blitz"

        st.markdown("<div class='royal-card'><h3>🛠️ تكوين الجمل</h3><p>بناء جمل إنجليزية</p></div>", unsafe_allow_html=True)
        if st.button("بدء بناء الجمل", use_container_width=True): st.session_state.page = "sentences"

# الغرفة (3): القاموس (المكتبة من الملف)
elif st.session_state.page == "dictionary":
    st.markdown("<h2 class='gold-text' style='text-align:center;'>📖 المكتبة الملكية (1011 كلمة)</h2>", unsafe_allow_html=True)
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()
    
    search = st.text_input("🔍 ابحث عن كلمة إنجليزية أو عربية من ملفك:").lower()
    for i, w in enumerate(st.session_state.db):
        if search in w['English'].lower() or search in w['Arabic']:
            cols = st.columns([3, 1])
            cols[0].write(f"**{w['English']}** = {w['Arabic']}")
            if cols[1].button("🔊", key=f"voice_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['English']}&type=2")

# الغرفة (4): الملف الشخصي
elif st.session_state.page == "profile":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>👤 ملفك الشخصي</h1></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='royal-card'><h3>إجمالي النقاط: {st.session_state.score}</h3></div>", unsafe_allow_html=True)
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()

# الغرفة (5): غرفة الاسترخاء
elif st.session_state.page == "relax":
    st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 غرفة الاسترخاء</h2></div>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()

# الغرفة (6): تحدي 60 ثانية
elif st.session_state.page == "blitz":
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("انتهى الوقت!"); st.button("رجوع", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h2 style='color:red; text-align:center;'>⏳ {rem} ثانية</h2>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("الإجابة:", key="blitz_in").strip() == word['Arabic']:
            st.session_state.score += 60; st.rerun()

# الغرفة (7): تكوين الجمل
elif st.session_state.page == "sentences":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>It is a good __.</h3><p>المطلوب كلمة: {word['Arabic']}</p></div>", unsafe_allow_html=True)
    if st.text_input("أكمل الفراغ:").lower().strip() == word['English'].lower():
        st.success("أحسنت!"); st.session_state.score += 20; time.sleep(1); st.rerun()
    
