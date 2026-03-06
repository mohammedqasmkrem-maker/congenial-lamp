import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم البصري الخارق (صورة الجبال ثابتة وفخمة) ---
st.set_page_config(page_title="Abt Royal Academy", layout="centered")

st.markdown("""
    <style>
    /* تثبيت صورة الجبال لتملأ الخلفية */
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    /* الغرف الزجاجية الملكية */
    .royal-room {
        background: rgba(0, 0, 0, 0.85);
        padding: 30px; border-radius: 30px;
        border: 2px solid #D4AC0D; color: white;
        text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }
    /* كروت الكلمات الملونة حسب الصعوبة */
    .word-card {
        background: rgba(255, 255, 255, 0.07);
        padding: 15px; border-radius: 15px;
        margin: 12px 0; border-right: 8px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
    }
    /* الأزرار الملكية الضخمة */
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D, #B8860B) !important;
        color: black !important; font-weight: 900 !important;
        height: 60px !important; border-radius: 15px !important;
        font-size: 19px !important; border: none !important;
    }
    /* لوحة الإحصائيات */
    .stat-box {
        background: rgba(212, 172, 13, 0.1);
        padding: 15px; border-radius: 15px; border: 1px solid #D4AC0D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (قراءة الـ 1011 كلمة وتصنيفها) ---
@st.cache_data
def get_royal_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    data = []
    try:
        r = requests.get(url)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if " - " in line:
                    p = line.split(" - ")
                    eng = re.sub(r'[^a-zA-Z\s]', '', p[0]).strip()
                    ara = p[1].strip()
                    if eng and ara:
                        # تصنيف المستويات
                        lv = "سهل 🟢" if len(eng) <= 4 else "متوسط 🟡" if len(eng) <= 7 else "صعب 🔴"
                        data.append({"eng": eng, "ara": ara, "lv": lv})
        return data
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "سهل 🟢"}]

# --- 3. نظام الرتب والجوائز ---
if 'db' not in st.session_state: st.session_state.db = get_royal_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'read_count' not in st.session_state: st.session_state.read_count = 0
if 'page' not in st.session_state: st.session_state.page = "main"

def get_rank():
    s = st.session_state.score
    if s >= 2000: return "👑 إمبراطور القمة", "🏆 وسام الذهب"
    if s >= 1000: return "⚔️ جنرال الأكاديمية", "🥇 وسام الفضة"
    if s >= 500: return "🛡️ فارس الجبال", "🥈 وسام النحاس"
    return "🌲 مستكشف مبتدئ", "🥉 وسام البداية"

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. الغرف ---
with st.container():
    st.markdown('<div class="royal-room">', unsafe_allow_html=True)

    # الغرفة [1]: المدخل
    if st.session_state.page == "main":
        st.markdown("<h1 style='color:#D4AC0D;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
        st.write(f"المكتبة محملة بـ **{len(st.session_state.db)}** كلمة مصنفة ✅")
        
        if st.button("📖 القاموس المصنف (مستويات)"): st.session_state.page = "dict"; st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
            if st.button("⚔️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
        with c2:
            if st.button("🔥 تحدي 60 ثانية"): 
                st.session_state.start_t = time.time(); st.session_state.page = "blitz"
                st.session_state.q = random.choice(st.session_state.db); st.rerun()
            if st.button("🍃 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

    # الغرفة [2]: القاموس المستويات
    elif st.session_state.page == "dict":
        if st.button("🔙 العودة للمدخل"): st.session_state.page = "main"; st.rerun()
        st.markdown("<h2 style='color:#D4AC0D;'>📖 قاموس المستويات</h2>", unsafe_allow_html=True)
        
        lv_choice = st.radio("اختر الصعوبة:", ["الكل", "سهل 🟢", "متوسط 🟡", "صعب 🔴"], horizontal=True)
        search = st.text_input("🔍 ابحث في الـ 1011 كلمة:")
        
        filtered = [w for w in st.session_state.db if (lv_choice == "الكل" or w['lv'] == lv_choice) and (search.lower() in w['eng'].lower() or search in w['ara'])]
        
        for i, w in enumerate(filtered[:100]):
            c_txt, c_spk = st.columns([5, 1])
            with c_txt:
                st.markdown(f"<div class='word-card'><b>{w['eng']}</b> <small>{w['lv']}</small> <b>{w['ara']}</b></div>", unsafe_allow_html=True)
            with c_spk:
                if st.button("🔊", key=f"s_{i}"): 
                    speak(w['eng']); st.session_state.read_count += 1

    # الغرفة [3]: الملف الشخصي (الألقاب والجوائز)
    elif st.session_state.page == "profile":
        rank, badge = get_rank()
        st.markdown(f"<h1 style='color:#D4AC0D;'>👤 ملف البطل</h1><h2 style='margin-top:-20px;'>{rank}</h2>", unsafe_allow_html=True)
        st.write(f"🏅 الجائزة: {badge}")
        
        col1, col2 = st.columns(2)
        with col1: st.markdown(f"<div class='stat-box'>📖 كلمات قرأتها<br><h1>{st.session_state.read_count}</h1></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-box'>💰 نقاط الإنجاز<br><h1>{st.session_state.score}</h1></div>", unsafe_allow_html=True)
        
        if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()

    # الغرفة [4]: الاختبار
    elif st.session_state.page == "test":
        if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
        if 'tq' not in st.session_state: st.session_state.tq = random.choice(st.session_state.db)
        st.markdown(f"### ترجم الكلمة: <br><h1 style='color:#D4AC0D;'>{st.session_state.tq['eng']}</h1>", unsafe_allow_html=True)
        ans = st.text_input("الإجابة:")
        if st.button("تحقق ✅"):
            if ans.strip() == st.session_state.tq['ara']:
                st.success("إجابة إمبراطورية! +20 نقطة")
                st.session_state.score += 20; st.session_state.tq = random.choice(st.session_state.db)
                time.sleep(1); st.rerun()
            else: st.error("حاول ثانية")

    st.markdown('</div>', unsafe_allow_html=True)
                               
