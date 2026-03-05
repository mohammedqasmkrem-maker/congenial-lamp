import streamlit as st
import pandas as pd
import random
import time
import requests
import re
from io import StringIO

# --- 1. التصميم الجبلي الكامل ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .main-box {
        background: rgba(0, 0, 0, 0.85);
        padding: 25px; border-radius: 20px; border: 2px solid #D4AC0D; color: white;
    }
    .gold { color: #D4AC0D !important; font-weight: bold; text-align: center; }
    .stButton>button { background: #D4AC0D !important; color: black !important; font-weight: bold !important; border-radius: 12px !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك قراءة الـ 1011 كلمة (الحل النهائي) ---
@st.cache_data
def load_full_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    data = []
    try:
        r = requests.get(url)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if " - " in line:
                    p = line.split(" - ")
                    # تنظيف الأرقام والمسافات
                    eng = re.sub(r'^\d+\.\s*', '', p[0]).strip()
                    ara = p[1].strip()
                    if eng and ara:
                        data.append({"English": eng, "Arabic": ara})
        return data if data else [{"English": "Error", "Arabic": "خطأ في التحميل"}]
    except:
        return [{"English": "Check Internet", "Arabic": "افحص الاتصال"}]

# --- 3. إدارة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_full_vocab()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def speak(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. الغرف (كل غرفة في مكانها) ---
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    # الغرفة 1: الدعاء
    if st.session_state.page == "dua":
        st.markdown("<h1 class='gold'>✨ دعاء طلب العلم</h1><p style='text-align:center; font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
        if st.button("آمين - دخول القصر الجبلي"):
            st.session_state.page = "hall"; st.rerun()

    # الغرفة 2: القصر (القائمة)
    elif st.session_state.page == "hall":
        st.markdown(f"<h1 class='gold'>🏔️ قصر Abt الملكي 🏔️</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>المكتبة جاهزة: <b>{len(st.session_state.db)}</b> كلمة ✅</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📖 القاموس والنطق (1011)"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        with c2:
            if st.button("⏳ تحدي 60 ثانية"): 
                st.session_state.start_time = time.time()
                st.session_state.q = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("🛠️ تكوين الجمل"): st.session_state.page = "sentences"; st.rerun()
            if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # الغرفة 3: القاموس
    elif st.session_state.page == "dict":
        st.button("🔙 عودة") and setattr(st.session_state, 'page', 'hall')
        search = st.text_input("🔍 ابحث في الـ 1011 كلمة:")
        words = [w for w in st.session_state.db if search.lower() in w['English'].lower() or search in w['Arabic']]
        for i, w in enumerate(words[:50]):
            colA, colB = st.columns([4, 1])
            colA.write(f"**{w['English']}** = {w['Arabic']}")
            if colB.button("🔊", key=f"s{i}"): speak(w['English'])

    # الغرفة 4: تحدي 60 ثانية (مع التحقق)
    elif st.session_state.page == "blitz":
        st.button("🔙 انسحاب") and setattr(st.session_state, 'page', 'hall')
        rem = 60 - int(time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            q = st.session_state.q
            st.write(f"### ترجم: {q['English']}")
            ans = st.text_input("الإجابة:")
            if st.button("تحقق ✅"):
                if ans.strip() == q['Arabic']:
                    st.session_state.score += 50
                    st.session_state.q = random.choice(st.session_state.db)
                    st.success("صح!"); time.sleep(0.5); st.rerun()

    # الغرفة 5: تكوين الجمل
    elif st.session_state.page == "sentences":
        st.button("🔙 عودة") and setattr(st.session_state, 'page', 'hall')
        word = random.choice(st.session_state.db)
        st.write(f"### ضع كلمة ({word['Arabic']}) في جملة إنجليزية:")
        st.markdown(f"**Hint:** {word['English']}")
        user_s = st.text_input("اكتب الجملة هنا:")
        if st.button("تحقق من الجملة ✅") and word['English'].lower() in user_s.lower():
            st.success("بطل! جملة صحيحة"); st.session_state.score += 20

    # الغرفة 6: غرفة الاسترخاء
    elif st.session_state.page == "relax":
        st.button("🔙 عودة") and setattr(st.session_state, 'page', 'hall')
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")

    st.markdown('</div>', unsafe_allow_html=True)
        
