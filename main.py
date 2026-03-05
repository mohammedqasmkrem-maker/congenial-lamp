import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التصميم الملكي (نظام الغرف) ---
st.set_page_config(page_title="Abt Royal Rooms", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .room-container {
        background: rgba(0, 0, 0, 0.9);
        padding: 25px; border-radius: 30px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center;
    }
    .word-card {
        background: rgba(255, 255, 255, 0.07);
        padding: 15px; border-radius: 12px;
        margin: 10px 0; border-right: 5px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: bold !important;
        height: 60px !important; border-radius: 15px !important;
        font-size: 18px !important; margin-bottom: 10px; border: none !important;
    }
    .back-btn button { background: #333 !important; color: white !important; height: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الجلب (ضمان الـ 1011 كلمة) ---
@st.cache_data
def get_full_vocab():
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
    except: return [{"eng": "Error", "ara": "خطأ"}]

# --- 3. إدارة النظام ---
if 'db' not in st.session_state: st.session_state.db = get_full_vocab()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. الغرف الملكية ---
with st.container():
    st.markdown('<div class="room-container">', unsafe_allow_html=True)

    # الغرفة [1]: الدعاء
    if st.session_state.page == "dua":
        st.markdown("<h1 style='color:#D4AC0D;'>✨ بوابة العلم</h1>", unsafe_allow_html=True)
        st.write("اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
        if st.button("آمين - دخول القصر"):
            st.session_state.page = "hall"; st.rerun()

    # الغرفة [2]: المدخل الرئيسي
    elif st.session_state.page == "hall":
        st.markdown("<h1 style='color:#D4AC0D;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
        st.write(f"المكتبة محملة بالكامل: **{len(st.session_state.db)}** كلمة ✅")
        
        if st.button("📖 القاموس والمراجعة الشاملة"): st.session_state.page = "dict"; st.rerun()
        if st.button("⚔️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
        if st.button("🔥 تحدي الـ 60 ثانية"): 
            st.session_state.start_t = time.time()
            st.session_state.q = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # الغرفة [3]: القاموس اللانهائي (هنا الحل)
    elif st.session_state.page == "dict":
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("🔙 العودة للمدخل"): st.session_state.page = "hall"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='color:#D4AC0D;'>📖 قاموس الـ 1011 كلمة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن أي كلمة:")
        
        filtered = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        
        # التعديل هنا: زدنا عدد الكلمات المعروضة لـ 200 مع إمكانية البحث للوصول للباقي
        # هذا يضمن السرعة وفي نفس الوقت يعطيك كل الكلمات
        st.write(f"إجمالي النتائج: {len(filtered)}")
        for i, w in enumerate(filtered[:300]): # الآن يعرض لك 300 كلمة دفعة واحدة!
            col_txt, col_spk = st.columns([5, 1])
            with col_txt:
                st.markdown(f"""<div class="word-card">
                    <b>{w['eng']}</b> <span style="color:#D4AC0D;">{w['ara']}</span>
                </div>""", unsafe_allow_html=True)
            with col_spk:
                if st.button("🔊", key=f"dict_{i}"): speak(w['eng'])

    # الغرفة [4]: الاختبار
    elif st.session_state.page == "test":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        if 't_q' not in st.session_state: st.session_state.t_q = random.choice(st.session_state.db)
        tq = st.session_state.t_q
        st.write(f"## ما ترجمة: {tq['eng']}؟")
        ans = st.text_input("الإجابة:")
        if st.button("تحقق ✅"):
            if ans.strip() == tq['ara']:
                st.success("بطل!"); st.session_state.score += 20
                st.session_state.t_q = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("خطأ!")

    # الغرفة [5]: تحدي 60 ثانية
    elif st.session_state.page == "blitz":
        rem = 60 - int(time.time() - st.session_state.start_t)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("خروج", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            q = st.session_state.q
            st.write(f"### ترجم: {q['eng']}")
            ans = st.text_input("الإجابة:")
            if st.button("تحقق ✅"):
                if ans.strip() == q['ara']:
                    st.session_state.score += 50
                    st.session_state.q = random.choice(st.session_state.db)
                    st.rerun()
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()

    # الغرفة [6]: الملف الشخصي
    elif st.session_state.page == "profile":
        st.markdown("<h1 style='color:#D4AC0D;'>👤 ملفك الشخصي</h1>")
        st.write(f"نقاطك الحالية: {st.session_state.score}")
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()

    # الغرفة [7]: الاسترخاء
    elif st.session_state.page == "relax":
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    
