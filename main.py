import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التصميم البصري الخارق (ثيم الجبال الملكي) ---
st.set_page_config(page_title="Abt Royal Academy", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .main-room {
        background: rgba(0, 0, 0, 0.85);
        padding: 30px; border-radius: 25px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center; box-shadow: 0 15px 40px rgba(0,0,0,0.9);
    }
    .word-card {
        background: rgba(212, 172, 13, 0.15);
        padding: 15px; border-radius: 15px;
        margin: 10px 0; border: 1px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: bold !important;
        height: 60px !important; border-radius: 15px !important;
        font-size: 19px !important; border: none !important;
    }
    .profile-stat {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px; border-radius: 15px; margin: 5px;
        border-bottom: 3px solid #D4AC0D;
    }
    .back-btn button { background: #444 !important; color: white !important; height: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات الذكي (1011 كلمة + مستويات) ---
@st.cache_data
def load_all_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    data = []
    try:
        r = requests.get(url)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if " - " in line:
                    p = line.split(" - ")
                    eng = re.sub(r'^\d+\.\s*', '', p[0]).strip()
                    ara = p[1].strip()
                    if eng and ara:
                        # تصنيف تلقائي حسب طول الكلمة كمستوى مبدئي
                        level = "مبتدئ" if len(eng) <= 4 else "متوسط" if len(eng) <= 7 else "متقدم"
                        data.append({"eng": eng, "ara": ara, "lv": level})
        return data
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "مبتدئ"}]

# --- 3. نظام الجلسة وتتبع الإنجاز ---
if 'db' not in st.session_state: st.session_state.db = load_all_data()
if 'page' not in st.session_state: st.session_state.page = "main"
if 'score' not in st.session_state: st.session_state.score = 0
if 'words_read' not in st.session_state: st.session_state.words_read = 0
if 'tests_done' not in st.session_state: st.session_state.tests_done = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

def get_rank():
    s = st.session_state.score
    if s >= 2000: return "🏔️ إمبراطور الجبال"
    if s >= 1000: return "👑 ملك القمة"
    if s >= 500: return "⚔️ فارس الأكاديمية"
    return "🌲 مستكشف مبتدئ"

# --- 4. تنفيذ الغرف الملكية ---
with st.container():
    st.markdown('<div class="main-room">', unsafe_allow_html=True)

    # --- القصر الرئيسي ---
    if st.session_state.page == "main":
        st.markdown("<h1 style='color:#D4AC0D;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
        st.write(f"المكتبة محملة: {len(st.session_state.db)} كلمة")
        
        if st.button("🚪 غرفة القاموس المستويات"): st.session_state.page = "dict"; st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⚔️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        with c2:
            if st.button("🔥 تحدي 60 ثانية"): 
                st.session_state.start_t = time.time()
                st.session_state.q = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("🍃 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # --- غرفة القاموس (مقسم مستويات) ---
    elif st.session_state.page == "dict":
        st.button("🔙 عودة", key="b1", on_click=lambda: setattr(st.session_state, 'page', 'main'))
        st.markdown("<h2 style='color:#D4AC0D;'>📖 القاموس المصنف</h2>", unsafe_allow_html=True)
        
        lvl = st.selectbox("اختر المستوى:", ["الكل", "مبتدئ", "متوسط", "متقدم"])
        search = st.text_input("🔍 ابحث عن كلمة:")
        
        filtered = [w for w in st.session_state.db if (lvl == "الكل" or w['lv'] == lvl) and (search.lower() in w['eng'].lower() or search in w['ara'])]
        
        for i, w in enumerate(filtered[:50]):
            col_txt, col_spk = st.columns([5, 1])
            with col_txt:
                st.markdown(f"<div class='word-card'><b>{w['eng']}</b> <span>[{w['lv']}]</span> <b>{w['ara']}</b></div>", unsafe_allow_html=True)
            with col_spk:
                if st.button("🔊", key=f"s{i}"): 
                    speak(w['eng'])
                    st.session_state.words_read += 1

    # --- غرفة الملف الشخصي (لوحة الإنجازات) ---
    elif st.session_state.page == "profile":
        st.markdown("<h2 style='color:#D4AC0D;'>👤 لوحة إنجازات البطل</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>الرتبة: <span style='color:#D4AC0D;'>{get_rank()}</span></h3>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='profile-stat'>📖 كلمات قرأتها<br><h2>{st.session_state.words_read}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='profile-stat'>⚔️ اختبارات ناجحة<br><h2>{st.session_state.tests_done}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='profile-stat'>💰 مجموع النقاط<br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.write("🏆 الجوائز: " + ("🥇 وسام القمة" if st.session_state.score > 500 else "⏳ قيد الإنجاز"))
        st.button("🔙 عودة للقصر", on_click=lambda: setattr(st.session_state, 'page', 'main'))

    # --- غرفة الاختبار ---
    elif st.session_state.page == "test":
        st.button("🔙 عودة", key="b2", on_click=lambda: setattr(st.session_state, 'page', 'main'))
        if 'tq' not in st.session_state: st.session_state.tq = random.choice(st.session_state.db)
        
        st.markdown(f"### ما ترجمة: <span style='color:#D4AC0D;'>{st.session_state.tq['eng']}</span>؟")
        ans = st.text_input("أدخل الترجمة العربية:")
        if st.button("تحقق ✅"):
            if ans.strip() == st.session_state.tq['ara']:
                st.success("إجابة ملكية! +20 نقطة")
                st.session_state.score += 20
                st.session_state.tests_done += 1
                st.session_state.tq = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("حاول مرة أخرى يا بطل")

    # --- غرفة الاسترخاء ---
    elif st.session_state.page == "relax":
        st.button("🔙 عودة", on_click=lambda: setattr(st.session_state, 'page', 'main'))
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")

    st.markdown('</div>', unsafe_allow_html=True)
