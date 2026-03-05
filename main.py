import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.98); z-index: -1; }
    .royal-card { background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; color: white; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. جلب الكلمات من ملف vocab.csv الحقيقي ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة الملف وتنظيف الأرقام (مثل 1. Time)
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Success", "Arabic": "نجاح"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 4. نظام الغرف المنفصلة ---

# الغرفة (1): الدعاء
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر", use_container_width=True):
        st.session_state.page = "hall"; st.rerun()

# الغرفة (2): القصر (القائمة الرئيسية)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 الملف الشخصي الحقيقي", use_container_width=True): st.session_state.page = "profile"; st.rerun()
        if st.button("📖 القاموس الملكي", use_container_width=True): st.session_state.page = "dictionary"; st.rerun()
        if st.button("✍️ اختبار الكلمات (بدون وقت)", use_container_width=True): st.session_state.page = "normal_test"; st.rerun()

    with col2:
        if st.button("⏳ تحدي الـ 60 ثانية (ذكاء)", use_container_width=True): 
            st.session_state.start_time = time.time(); st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ بناء الجمل الذكي", use_container_width=True): st.session_state.page = "sentences"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء", use_container_width=True): st.session_state.page = "relax"; st.rerun()

# الغرفة (3): الملف الشخصي
elif st.session_state.page == "profile":
    st.markdown(f"<div class='royal-card'><h1>👤 ملفك الحقيقي</h1><h2>إجمالي نقاطك: {st.session_state.score}</h2></div>", unsafe_allow_html=True)
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()

# الغرفة (4): القاموس (المكتبة)
elif st.session_state.page == "dictionary":
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 المكتبة الشاملة</h2>", unsafe_allow_html=True)
    search = st.text_input("بحث بالإنجليزية أو العربية:")
    for w in st.session_state.db[:100]:
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            st.write(f"**{w['English']}** = {w['Arabic']}")

# الغرفة (5): اختبار الكلمات (العادي)
elif st.session_state.page == "normal_test":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    if 'test_w' not in st.session_state: st.session_state.test_w = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h2>{st.session_state.test_w['English']}</h2></div>", unsafe_allow_html=True)
    ans = st.text_input("ما ترجمتها؟")
    if st.button("تحقق ✅"):
        if ans.strip() == st.session_state.test_w['Arabic']:
            st.success("صح! +10 نقاط"); st.session_state.score += 10
            st.session_state.test_w = random.choice(st.session_state.db); time.sleep(1); st.rerun()

# الغرفة (6): تحدي الـ 60 ثانية
elif st.session_state.page == "blitz":
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("عودة للقصر", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h2 style='color:red;'>⏳ {rem} ثانية</h2>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("الإجابة:", key="speed").strip() == word['Arabic']:
            st.session_state.score += 60; st.rerun()

# الغرفة (7): بناء الجمل
elif st.session_state.page == "sentences":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>The __ is very important.</h3><p>(المطلوب: {word['Arabic']})</p></div>", unsafe_allow_html=True)
    if st.text_input("أكمل الفراغ بالإنجليزية:").lower().strip() == word['English'].lower():
        st.success("أحسنت!"); st.session_state.score += 20; time.sleep(1); st.rerun()

# الغرفة (8): غرفة الاسترخاء
elif st.session_state.page == "relax":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
                   
