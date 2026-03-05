import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.95); z-index: -1; }
    .royal-card { background: rgba(20, 35, 30, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; color: white; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. جلب البيانات ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.dropna().to_dict('records')
    except: return [{"English": "Time", "Arabic": "الوقت"}]

# --- 3. تهيئة النظام ---
for key in ['score', 'page', 'show_dua']:
    if key not in st.session_state:
        st.session_state.score = 0; st.session_state.page = "hall"; st.session_state.show_dua = True
if 'db' not in st.session_state: st.session_state.db = load_data()

# --- 4. التنقل بين الغرف ---
if st.session_state.show_dua:
    st.markdown("<div class='royal-card'><h2 class='gold-text'>✨ دعاء العلم</h2><p>اللهم علمني ما ينفعني</p></div>", unsafe_allow_html=True)
    if st.button("دخول القصر"): st.session_state.show_dua = False; st.rerun()

elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    # توزيع الأزرار حسب طلبك
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown("<div class='royal-card'><h3>📖 القاموس</h3></div>", unsafe_allow_html=True)
            if st.button("فتح المكتبة", use_container_width=True): st.session_state.page = "dict"
        
        with st.container():
            st.markdown("<div class='royal-card'><h3>✍️ اختبار كلمات</h3><p>بدون وقت</p></div>", unsafe_allow_html=True)
            if st.button("بدء الاختبار العادي", use_container_width=True): st.session_state.page = "normal_test"

    with col2:
        with st.container():
            st.markdown("<div class='royal-card'><h3>⏳ تحدي 60 ثانية</h3><p>ذكاء اصطناعي</p></div>", unsafe_allow_html=True)
            if st.button("ابدأ تحدي السرعة", use_container_width=True): 
                st.session_state.start_time = time.time(); st.session_state.page = "speed_test"

        with st.container():
            st.markdown("<div class='royal-card'><h3>🛠️ تكوين الجمل</h3></div>", unsafe_allow_html=True)
            if st.button("بناء الجمل الملكية", use_container_width=True): st.session_state.page = "sentence_test"

# --- 5. منطق الغرف (كل واحدة مستقلة) ---

# 1. القاموس (بحث فقط)
if st.session_state.page == "dict":
    st.markdown("<h2 class='gold-text'>📖 القاموس الملكي</h2>", unsafe_allow_html=True)
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    search = st.text_input("بحث بالإنجليزية:")
    for w in st.session_state.db:
        if search.lower() in w['English'].lower():
            st.write(f"**{w['English']}** = {w['Arabic']}")

# 2. اختبار كلمات (بدون وقت)
elif st.session_state.page == "normal_test":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h2>{word['English']}</h2></div>", unsafe_allow_html=True)
    ans = st.text_input("ما الترجمة العربية؟")
    if st.button("تحقق"):
        if ans == word['Arabic']: st.success("صح!"); time.sleep(1); st.rerun()

# 3. تحدي 60 ثانية (الذكاء الاصطناعي)
elif st.session_state.page == "speed_test":
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("انتهى الوقت!"); st.button("العودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h2 style='color:red;'>⏳ {rem}</h2>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("الإجابة:", key="speed").strip() == word['Arabic']: 
            st.session_state.score += 60; st.rerun()

# 4. تكوين الجمل (وحدها)
elif st.session_state.page == "sentence_test":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>The __ is very important.</h3><p>(المطلوب كلمة: {word['Arabic']})</p></div>", unsafe_allow_html=True)
    if st.text_input("أكمل الفراغ بالإنجليزية:").lower() == word['English'].lower():
        st.success("جملة رائعة!"); time.sleep(1); st.rerun()
    
