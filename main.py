import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. التصميم الجديد (واجهة عصرية غامقة) ---
st.set_page_config(page_title="Abt Academy v3", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    /* حاوية الغرف */
    .room-box {
        background: rgba(15, 15, 15, 0.95);
        padding: 20px; border-radius: 25px;
        border: 1px solid #D4AC0D; color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    /* كروت الكلمات */
    .word-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px; border-radius: 15px;
        margin-bottom: 10px; border-right: 5px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
    }
    /* الأزرار الملكية */
    .stButton>button {
        background: #D4AC0D !important; color: black !important;
        font-weight: bold !important; border-radius: 12px !important;
        border: none !important; width: 100%; height: 50px;
    }
    .nav-btn button {
        background: #333 !important; color: white !important;
        height: 35px !important; font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب البيانات (1011 كلمة) ---
@st.cache_data
def load_data():
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
        return data
    except: return [{"eng": "Error", "ara": "خطأ"}]

# --- 3. الجلسة والتنقل ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'dict_page' not in st.session_state: st.session_state.dict_page = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. الغرف ---
with st.container():
    st.markdown('<div class="room-box">', unsafe_allow_html=True)

    # --- الغرفة 1: الدعاء ---
    if st.session_state.page == "dua":
        st.markdown("<h2 style='text-align:center; color:#D4AC0D;'>✨ دعاء البداية</h2>", unsafe_allow_html=True)
        st.write("اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
        if st.button("آمين - دخول الأكاديمية"):
            st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 2: القصر الرئيسي ---
    elif st.session_state.page == "hall":
        st.markdown("<h1 style='text-align:center; color:#D4AC0D;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
        st.write(f"المكتبة محملة: {len(st.session_state.db)} كلمة")
        
        if st.button("📖 القاموس (نظام الصفحات)"): st.session_state.page = "dict"; st.rerun()
        
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

    # --- الغرفة 3: القاموس (نظام الصفحات) ---
    elif st.session_state.page == "dict":
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:#D4AC0D;'>📖 القاموس الملكي</h3>", unsafe_allow_html=True)
        
        # البحث
        search = st.text_input("🔍 ابحث عن كلمة:")
        filtered = [w for w in st.session_state.db if search.lower() in w['eng'].lower() or search in w['ara']]
        
        # إعداد الصفحات (كل صفحة 10 كلمات عشان الموبايل)
        words_per_page = 10
        total_pages = (len(filtered) // words_per_page)
        
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("⬅️ السابق") and st.session_state.dict_page > 0:
                st.session_state.dict_page -= 1; st.rerun()
        with col_page:
            st.write(f"صفحة {st.session_state.dict_page + 1} من {total_pages + 1}")
        with col_next:
            if st.button("التالي ➡️") and st.session_state.dict_page < total_pages:
                st.session_state.dict_page += 1; st.rerun()

        start_idx = st.session_state.dict_page * words_per_page
        for i, w in enumerate(filtered[start_idx : start_idx + words_per_page]):
            col_txt, col_spk = st.columns([4, 1])
            with col_txt:
                st.markdown(f"<div class='word-card'><b>{w['eng']}</b> <span>{w['ara']}</span></div>", unsafe_allow_html=True)
            with col_spk:
                if st.button("🔊", key=f"v{i}"): speak(w['eng'])

    # --- الغرفة 4: اختبار التحقق ---
    elif st.session_state.page == "test":
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
        if 't_q' not in st.session_state: st.session_state.t_q = random.choice(st.session_state.db)
        tq = st.session_state.t_q
        st.markdown(f"<h3 style='text-align:center;'>ما معنى كلمة: <br><span style='color:#D4AC0D;'>{tq['eng']}</span></h3>", unsafe_allow_html=True)
        ans = st.text_input("الإجابة العربية:")
        if st.button("تحقق ✅"):
            if ans.strip() == tq['ara']:
                st.success("إجابة صحيحة!"); st.session_state.score += 10
                st.session_state.t_q = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("خطأ، حاول مرة ثانية")

    # --- الغرفة 5: تحدي الـ 60 ثانية ---
    elif st.session_state.page == "blitz":
        elapsed = int(time.time() - st.session_state.start_t)
        if elapsed >= 60:
            st.error("انتهى الوقت!"); st.button("عودة للقصر", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h2 style='color:red; text-align:center;'>⏳ {60 - elapsed}</h2>", unsafe_allow_html=True)
            q = st.session_state.q
            st.write(f"### ترجم: {q['eng']}")
            ans = st.text_input("الترجمة:")
            if st.button("تحقق ✅"):
                if ans.strip() == q['ara']:
                    st.session_state.score += 50
                    st.session_state.q = random.choice(st.session_state.db)
                    st.success("أحسنت!"); time.sleep(0.3); st.rerun()
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 6: الملف الشخصي ---
    elif st.session_state.page == "profile":
        st.markdown("<h2 style='text-align:center; color:#D4AC0D;'>👤 ملف البطل</h2>", unsafe_allow_html=True)
        st.write(f"مجموع نقاطك: {st.session_state.score}")
        if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()

    # --- الغرفة 7: الاسترخاء ---
    elif st.session_state.page == "relax":
        st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
        if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
