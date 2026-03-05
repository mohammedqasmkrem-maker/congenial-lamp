import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التصميم السينمائي (نظام الغرف) ---
st.set_page_config(page_title="Abt Royal Rooms", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    /* حاوية الغرفة الواحدة */
    .room-container {
        background: rgba(0, 0, 0, 0.9);
        padding: 30px; border-radius: 30px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }
    /* كروت الكلمات الفخمة */
    .word-card {
        background: linear-gradient(to right, rgba(212,172,13,0.1), rgba(0,0,0,0.5));
        padding: 20px; border-radius: 15px;
        margin: 15px 0; border-left: 6px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
        font-size: 22px;
    }
    /* أزرار الغرف الكبيرة */
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: bold !important;
        height: 65px !important; border-radius: 18px !important;
        font-size: 20px !important; margin-bottom: 15px;
        border: none !important; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 5px 15px #D4AC0D; }
    .back-btn button { background: #222 !important; color: white !important; height: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة (بدون أخطاء) ---
@st.cache_data
def get_clean_data():
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
        return words
    except: return [{"eng": "Network Error", "ara": "خطأ اتصال"}]

# --- 3. إدارة الجلسة ---
if 'db' not in st.session_state: st.session_state.db = get_clean_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. الدخول إلى الغرف ---
with st.container():
    st.markdown('<div class="room-container">', unsafe_allow_html=True)

    # --- الغرفة [1]: دعاء طلب العلم ---
    if st.session_state.page == "dua":
        st.markdown("<h1 style='color:#D4AC0D;'>✨ بوابه العلم</h1>", unsafe_allow_html=True)
        st.write("اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
        if st.button("آمين - دخول القصر"):
            st.session_state.page = "hall"; st.rerun()

    # --- الغرفة [2]: القصر الرئيسي (المدخل) ---
    elif st.session_state.page == "hall":
        st.markdown("<h1 style='color:#D4AC0D;'>🏔️ مدخل القصر الملكي</h1>", unsafe_allow_html=True)
        st.write(f"المكتبة محملة بـ {len(st.session_state.db)} كلمة")
        st.write("---")
        
        # أزرار الغرف
        if st.button("🚪 غرفة القاموس والمراجعة"): st.session_state.page = "dict"; st.rerun()
        if st.button("⚔️ غرفة الاختبار الذكي"): st.session_state.page = "test"; st.rerun()
        if st.button("🔥 غرفة تحدي الـ 60 ثانية"): 
            st.session_state.start_t = time.time()
            st.session_state.q = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("👤 غرفة الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        if st.button("🍃 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # --- الغرفة [3]: غرفة القاموس (تصميم كروت المراجعة) ---
    elif st.session_state.page == "dict":
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("🔙 مغادرة الغرفة والعودة للمدخل"): st.session_state.page = "hall"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='color:#D4AC0D;'>📖 مراجعة الـ 1011 كلمة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في القاموس...")
        
        filtered = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        
        for i, w in enumerate(filtered[:50]): # عرض 50 في كل مرة لضمان السرعة
            col_txt, col_spk = st.columns([5, 1])
            with col_txt:
                st.markdown(f"""<div class="word-card">
                    <span style="font-weight:bold;">{w['eng']}</span>
                    <span style="color:#D4AC0D;">{w['ara']}</span>
                </div>""", unsafe_allow_html=True)
            with col_spk:
                st.write("") # للمسافة
                if st.button("🔊", key=f"v{i}"): speak(w['eng'])

    # --- الغرفة [4]: غرفة الاختبار ---
    elif st.session_state.page == "test":
        if st.button("🔙 عودة للمدخل"): st.session_state.page = "hall"; st.rerun()
        if 't_q' not in st.session_state: st.session_state.t_q = random.choice(st.session_state.db)
        tq = st.session_state.t_q
        st.markdown(f"### ما معنى كلمة: <br><span style='font-size:40px; color:#D4AC0D;'>{tq['eng']}</span>", unsafe_allow_html=True)
        ans = st.text_input("اكتب الترجمة العربية:")
        if st.button("تحقق من الإجابة ✅"):
            if ans.strip() == tq['ara']:
                st.success("بطل! إجابة صحيحة"); st.session_state.score += 20
                st.session_state.t_q = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("خطأ، ركز وحاول مرة ثانية")

    # --- الغرفة [5]: غرفة تحدي 60 ثانية ---
    elif st.session_state.page == "blitz":
        rem = 60 - int(time.time() - st.session_state.start_t)
        if rem <= 0:
            st.error("💥 انتهى الوقت!"); st.button("خروج", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            q = st.session_state.q
            st.write(f"## ترجم بسرعة: {q['eng']}")
            ans = st.text_input("الإجابة:")
            if st.button("تحقق ✅"):
                if ans.strip() == q['ara']:
                    st.session_state.score += 50
                    st.session_state.q = random.choice(st.session_state.db)
                    st.rerun()
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة [6]: غرفة الملف الشخصي ---
    elif st.session_state.page == "profile":
        st.markdown("<h1 style='color:#D4AC0D;'>👤 ملف البطل</h1>", unsafe_allow_html=True)
        st.write(f"نقاطك الحالية: {st.session_state.score}")
        if st.button("🔙 العودة للمدخل"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة [7]: غرفة الاسترخاء ---
    elif st.session_state.page == "relax":
        st.markdown("### 🍃 استراحة المحارب")
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
        if st.button("🔙 العودة للمدخل"): st.session_state.page = "hall"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    
