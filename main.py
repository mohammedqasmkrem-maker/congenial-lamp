import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التنسيق البصري (فخامة الجبيلة والجبال) ---
st.set_page_config(page_title="Abt Royal Academy", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .glass-room {
        background: rgba(0, 0, 0, 0.92);
        padding: 25px; border-radius: 20px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center;
    }
    .dictionary-card {
        background: rgba(255, 255, 255, 0.05);
        margin: 10px 0; padding: 15px;
        border-radius: 12px; border-right: 4px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: bold !important;
        border-radius: 10px !important; border: none !important;
    }
    .nav-btn button { background: #333 !important; color: white !important; height: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة (ربط vocab.csv) ---
@st.cache_data
def load_data():
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
    except: return [{"eng": "Welcome", "ara": "أهلاً"}]

# --- 3. إدارة التنقل ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. غرف القصر الملكي ---
with st.container():
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)

    # --- الغرفة 0: دعاء البداية ---
    if st.session_state.page == "dua":
        st.markdown("<h1 style='color:#D4AC0D;'>✨ فاتحة العلم</h1>", unsafe_allow_html=True)
        st.write("اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
        if st.button("آمين - دخول القصر"):
            st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 1: القصر الرئيسي ---
    elif st.session_state.page == "hall":
        st.markdown("<h2 style='color:#D4AC0D;'>🏔️ قصر Abt الملكي</h2>", unsafe_allow_html=True)
        st.write(f"تم ربط {len(st.session_state.db)} كلمة للمراجعة ✅")
        
        if st.button("📖 القاموس والمراجعة الشاملة"): st.session_state.page = "dict"; st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✍️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
        with col2:
            if st.button("⏳ تحدي 60 ثانية"): 
                st.session_state.start_t = time.time()
                st.session_state.q = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
        
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # --- الغرفة 2: القاموس (المراجعة مثل السمعة) ---
    elif st.session_state.page == "dict":
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:#D4AC0D;'>📖 مراجعة الكلمات (السمعة)</h3>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن كلمة معينة:")
        
        filtered = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        
        # عرض الكلمات بتصميم بطاقات مرتبة
        for i, w in enumerate(filtered[:100]): # نعرض 100 لتجنب الثقل
            col_txt, col_spk = st.columns([4, 1])
            with col_txt:
                st.markdown(f"""<div class="dictionary-card">
                    <div><b>{w['eng']}</b></div>
                    <div style="color:#D4AC0D;">{w['ara']}</div>
                </div>""", unsafe_allow_html=True)
            with col_spk:
                st.write("") # موازنة
                if st.button("🔊", key=f"v{i}"): speak(w['eng'])

    # --- الغرفة 3: اختبار التحقق ---
    elif st.session_state.page == "test":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        if 't_q' not in st.session_state: st.session_state.t_q = random.choice(st.session_state.db)
        tq = st.session_state.t_q
        st.write(f"### ما معنى: **{tq['eng']}**؟")
        ans = st.text_input("الترجمة:")
        if st.button("تحقق ✅"):
            if ans.strip() == tq['ara']:
                st.success("صح! بطل"); st.session_state.score += 10
                st.session_state.t_q = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("خطأ، حاول ثانية")

    # --- الغرفة 4: الملف الشخصي ---
    elif st.session_state.page == "profile":
        st.markdown("<h2 style='color:#D4AC0D;'>👤 ملف البطل</h2>", unsafe_allow_html=True)
        st.write(f"النقاط الحالية: {st.session_state.score}")
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 5: الاسترخاء ---
    elif st.session_state.page == "relax":
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
            
