import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التصميم الجبلي الفخم (نظام الغرف) ---
st.set_page_config(page_title="Abt Royal Academy", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .glass-room {
        background: rgba(0, 0, 0, 0.9);
        padding: 30px; border-radius: 25px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: bold !important;
        height: 55px !important; border-radius: 15px !important;
        font-size: 18px !important; width: 100%; border: none !important;
    }
    .back-btn button { background: #333 !important; color: white !important; height: 40px !important; }
    .stat-card { background: rgba(212, 172, 13, 0.1); padding: 15px; border-radius: 15px; border: 1px solid #D4AC0D; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة (الربط الحديدي) ---
@st.cache_data
def load_royal_data():
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
                    if eng and ara: data.append({"eng": eng, "ara": ara})
        return data if data else [{"eng": "Success", "ara": "نجاح"}]
    except: return [{"eng": "Error", "ara": "خطأ"}]

# --- 3. إدارة الجلسة ---
if 'db' not in st.session_state: st.session_state.db = load_royal_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'rank' not in st.session_state: st.session_state.rank = "مبتدئ جبلي 🌲"

def check_rank():
    s = st.session_state.score
    if s > 1000: st.session_state.rank = "ملك الجبال 👑"
    elif s > 500: st.session_state.rank = "فارس الأكاديمية ⚔️"
    elif s > 200: st.session_state.rank = "مغامر محترف 🏔️"

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. تنفيذ الغرف الملكية ---
with st.container():
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)

    # --- الغرفة 1: دعاء البداية ---
    if st.session_state.page == "dua":
        st.markdown("<h1 style='color:#D4AC0D;'>✨ فاتحة العلم</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
        if st.button("آمين - دخول القصر"):
            st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 2: القصر (المنطقة المركزية) ---
    elif st.session_state.page == "hall":
        st.markdown("<h1 style='color:#D4AC0D;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
        st.write(f"المكتبة جاهزة بـ {len(st.session_state.db)} كلمة")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 القاموس"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
        with col2:
            if st.button("⏳ تحدي الـ 60 ثانية"): 
                st.session_state.start_t = time.time()
                st.session_state.q = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # --- الغرفة 3: القاموس ---
    elif st.session_state.page == "dict":
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في الـ 1011 كلمة:")
        filtered = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        for i, w in enumerate(filtered[:50]):
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['eng']}** = {w['ara']}")
            if c2.button("🔊", key=f"v{i}"): speak(w['eng'])

    # --- الغرفة 4: اختبار التحقق ---
    elif st.session_state.page == "test":
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if 't_word' not in st.session_state: st.session_state.t_word = random.choice(st.session_state.db)
        tw = st.session_state.t_word
        st.write(f"### ما معنى كلمة: **{tw['eng']}**؟")
        ans = st.text_input("اكتب الترجمة العربية:")
        if st.button("تحقق ✅"):
            if ans.strip() == tw['ara']:
                st.success("إجابة صحيحة! +20 نقطة")
                st.session_state.score += 20; check_rank()
                st.session_state.t_word = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("حاول مرة أخرى")

    # --- الغرفة 5: تحدي الـ 60 ثانية ---
    elif st.session_state.page == "blitz":
        rem = 60 - int(time.time() - st.session_state.start_t)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h2 style='color:red;'>⏳ {rem}</h2>", unsafe_allow_html=True)
            q = st.session_state.q
            st.write(f"### ترجم بسرعة: {q['eng']}")
            ans = st.text_input("الترجمة:")
            if st.button("تحقق ✅"):
                if ans.strip() == q['ara']:
                    st.session_state.score += 50; check_rank()
                    st.session_state.q = random.choice(st.session_state.db)
                    st.success("أحسنت!"); time.sleep(0.3); st.rerun()
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 6: الملف الشخصي ---
    elif st.session_state.page == "profile":
        st.markdown("<h1 style='color:#D4AC0D;'>👤 ملف البطل الملكي</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='stat-card'>
            <h3>مرحباً بك يا محمد</h3>
            <p style='font-size:20px;'>مجموع نقاطك: <b>{st.session_state.score}</b></p>
            <p style='font-size:20px;'>رتبتك الحالية: <b>{st.session_state.rank}</b></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 7: غرفة الاسترخاء ---
    elif st.session_state.page == "relax":
        st.markdown("<h3>🌿 وقت الاسترخاء والهدوء</h3>", unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
                
