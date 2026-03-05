import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التصميم الملكي (واجهة غرف موبايل) ---
st.set_page_config(page_title="Abt Royal Academy", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .room-container {
        background: rgba(0, 0, 0, 0.85);
        padding: 25px; border-radius: 20px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center;
    }
    .menu-btn button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: bold !important;
        height: 60px !important; border-radius: 15px !important;
        font-size: 20px !important; margin-bottom: 10px;
    }
    .back-btn button { background: #444 !important; color: white !important; }
    .word-card {
        background: rgba(255,255,255,0.1); padding: 10px;
        border-radius: 10px; margin: 5px 0; border-left: 5px solid #D4AC0D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة (بدون ضياع) ---
@st.cache_data
def get_all_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    words = []
    try:
        r = requests.get(url)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if " - " in line:
                    p = line.split(" - ")
                    eng = re.sub(r'^\d+\.\s*', '', p[0]).strip()
                    ara = p[1].strip()
                    if eng and ara: words.append({"eng": eng, "ara": ara})
        return words if words else [{"eng": "Time", "ara": "الوقت"}]
    except: return [{"eng": "Error", "ara": "خطأ اتصال"}]

# --- 3. نظام الجلسة ---
if 'db' not in st.session_state: st.session_state.db = get_all_data()
if 'page' not in st.session_state: st.session_state.page = "main"
if 'score' not in st.session_state: st.session_state.score = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. تنفيذ الغرف ---
with st.container():
    st.markdown('<div class="room-container">', unsafe_allow_html=True)

    # --- الغرفة الرئيسية ---
    if st.session_state.page == "main":
        st.markdown("<h1 style='color:#D4AC0D;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
        st.write(f"✅ تم تحميل {len(st.session_state.db)} كلمة بنجاح")
        
        st.markdown('<div class="menu-btn">', unsafe_allow_html=True)
        if st.button("📖 القاموس الذكي (1011)"): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
        if st.button("⏳ تحدي الـ 60 ثانية"): 
            st.session_state.start_t = time.time()
            st.session_state.q = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("👤 ملف البطل"): st.session_state.page = "profile"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- غرفة القاموس (بنظام الصفحات للسرعة) ---
    elif st.session_state.page == "dict":
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("🔙 العودة للقصر"): st.session_state.page = "main"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        search = st.text_input("🔍 ابحث عن كلمة:")
        filtered = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        
        # تقسيم القاموس لصفحات لكي لا يعلق التطبيق
        page_num = st.number_input("الصفحة", min_value=1, max_value=(len(filtered)//20)+1, step=1)
        start = (page_num - 1) * 20
        end = start + 20
        
        for i, w in enumerate(filtered[start:end]):
            with st.container():
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"<div class='word-card'><b>{w['eng']}</b> = {w['ara']}</div>", unsafe_allow_html=True)
                if col2.button("🔊", key=f"v{i}"): speak(w['eng'])

    # --- غرفة تحدي الـ 60 ثانية ---
    elif st.session_state.page == "blitz":
        rem = 60 - int(time.time() - st.session_state.start_t)
        if rem <= 0:
            st.error("💥 انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'main'))
        else:
            st.markdown(f"<h2 style='color:red;'>⏳ {rem} ثانية</h2>", unsafe_allow_html=True)
            q = st.session_state.q
            st.write(f"### ترجم: {q['eng']}")
            ans = st.text_input("الإجابة العربية:")
            if st.button("تحقق ✅"):
                if ans.strip() == q['ara']:
                    st.session_state.score += 50
                    st.session_state.q = random.choice(st.session_state.db)
                    st.success("صح! +50"); time.sleep(0.4); st.rerun()
                else: st.error("خطأ، حاول ثانية")
        if st.button("🔙 انسحاب"): st.session_state.page = "main"; st.rerun()

    # --- غرفة الاسترخاء ---
    elif st.session_state.page == "relax":
        if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")

    st.markdown('</div>', unsafe_allow_html=True)
        
