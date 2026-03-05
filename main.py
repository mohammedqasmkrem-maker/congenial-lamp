import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. الإعدادات الملكية والخلفية الجبلية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* خلفية جبلية كاملة */
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    /* حاوية المحتوى الزجاجية */
    .glass-panel {
        background: rgba(0, 0, 0, 0.88);
        padding: 30px;
        border-radius: 25px;
        border: 2px solid #D4AC0D;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .gold-title { color: #D4AC0D; text-align: center; font-size: 40px; font-weight: bold; text-shadow: 2px 2px 10px black; }
    .stButton>button {
        background: linear-gradient(45deg, #D4AC0D, #F1C40F) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        height: 50px;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px #D4AC0D; }
    .back-btn>button { background: #666 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة (بدون توقف) ---
@st.cache_data
def fetch_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    final_db = []
    try:
        r = requests.get(url)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if " - " in line:
                    parts = line.split(" - ")
                    # تنظيف الإنجليزي من الأرقام والمسافات
                    eng = re.sub(r'^\d+\.\s*', '', parts[0]).strip()
                    ara = parts[1].strip()
                    if eng and ara:
                        final_db.append({"eng": eng, "ara": ara})
        return final_db if final_db else [{"eng": "Welcome", "ara": "أهلاً"}]
    except:
        return [{"eng": "Check Connection", "ara": "افحص الاتصال"}]

# --- 3. إدارة الحالة ---
if 'db' not in st.session_state: st.session_state.db = fetch_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def speak(text):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={text}&type=2")

# --- 4. نظام الغرف (التنفيذ) ---
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    # 1. غرفة الدعاء
    if st.session_state.page == "dua":
        st.markdown("<h1 class='gold-title'>✨ دعاء طلب العلم</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:25px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
        if st.button("آمين - دخول الأكاديمية الجبلية"):
            st.session_state.page = "hall"; st.rerun()

    # 2. القصر الرئيسي (القائمة)
    elif st.session_state.page == "hall":
        st.markdown("<h1 class='gold-title'>🏔️ قصر Abt الملكي 🏔️</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>المكتبة محملة بالكامل: <b style='color:#D4AC0D; font-size:20px;'>{len(st.session_state.db)}</b> كلمة ✅</p>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        with cols[0]:
            if st.button("📖 القاموس والنطق (1011)"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق الذكي"): st.session_state.page = "test"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        with cols[1]:
            if st.button("⏳ تحدي الـ 60 ثانية 🔥"): 
                st.session_state.start_t = time.time()
                st.session_state.q_word = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("🛠️ بناء الجمل الملكي"): st.session_state.page = "build"; st.rerun()
            if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # 3. القاموس (عرض شامل)
    elif st.session_state.page == "dict":
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        search = st.text_input("🔍 ابحث في الـ 1011 كلمة:")
        res = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        for i, w in enumerate(res[:100]):
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['eng']}** = {w['ara']}")
            if c2.button("🔊", key=f"v{i}"): speak(w['eng'])

    # 4. تحدي الـ 60 ثانية (تحقق + نطق)
    elif st.session_state.page == "blitz":
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
        timeLeft = 60 - int(time.time() - st.session_state.start_t)
        if timeLeft <= 0:
            st.error("💥 انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {timeLeft}</h1>", unsafe_allow_html=True)
            word = st.session_state.q_word
            st.markdown(f"<h2 style='text-align:center;'>ترجم: <span style='color:#D4AC0D;'>{word['eng']}</span></h2>", unsafe_allow_html=True)
            if st.button("اسمع النطق 🔊"): speak(word['eng'])
            ans = st.text_input("اكتب الترجمة العربية هنا:")
            if st.button("تحقق ✅"):
                if ans.strip() == word['ara']:
                    st.session_state.score += 50
                    st.session_state.q_word = random.choice(st.session_state.db)
                    st.success("إجابة صحيحة! +50 نقطة")
                    time.sleep(0.5); st.rerun()
                else: st.error("خطأ! حاول مرة أخرى")

    # 5. بناء الجمل
    elif st.session_state.page == "build":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        w = random.choice(st.session_state.db)
        st.write(f"### استخدم كلمة **{w['eng']}** ({w['ara']}) في جملة:")
        sentence = st.text_input("اكتب جملتك:")
        if st.button("تحقق من الجملة"):
            if w['eng'].lower() in sentence.lower():
                st.success("بطل! جملة مفيدة"); st.session_state.score += 30
            else: st.warning("الجملة يجب أن تحتوي على الكلمة المطلوبة")

    # 6. الاسترخاء
    elif st.session_state.page == "relax":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")

    # 7. الملف الشخصي
    elif st.session_state.page == "profile":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        st.markdown(f"<div style='text-align:center;'><h1>👤 ملف البطل</h1><h2>النقاط: {st.session_state.score}</h2><h3>الرتبة: ملك الجبال 👑</h3></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
                    
