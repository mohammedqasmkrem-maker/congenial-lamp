import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم الزجاجي (Glassmorphism) مع خلفية الجبال ---
st.set_page_config(page_title="Abt Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    /* الغرفة الزجاجية */
    .glass-card {
        background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 25px;
        padding: 30px; color: white; text-align: center;
        max-width: 850px; margin: auto; box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    /* الأزرار العصرية */
    .stButton>button {
        background: rgba(255, 255, 255, 0.15) !important; color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important; border-radius: 15px !important;
        height: 55px !important; font-size: 18px !important; font-weight: bold !important;
        width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background: rgba(255, 255, 255, 0.3) !important; transform: scale(1.02); }
    
    /* كروت الكلمات */
    .word-item {
        background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px;
        margin: 10px 0; border-left: 5px solid #D4AC0D;
        display: flex; justify-content: space-between; align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (المميزات البرمجية) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    final = []
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
                        lv = "سهل" if len(eng) <= 4 else "متوسط" if len(eng) <= 7 else "صعب"
                        final.append({"eng": eng, "ara": ara, "lv": lv})
        return final
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "سهل"}]

# --- 3. نظام الجلسة (إدارة الـ 20 ميزة) ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'read_count' not in st.session_state: st.session_state.read_count = 0
if 'test_q' not in st.session_state: st.session_state.test_q = None

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. الغرف التنفيذية ---

# [1] غرفة الدعاء
if st.session_state.page == "dua":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>✨ دعاء طلب العلم</h1>", unsafe_allow_html=True)
    st.write("### اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
    if st.button("آمين - دخول الأكاديمية"):
        st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [2] القاعة الرئيسية
elif st.session_state.page == "main":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>🏔️ أكاديمية أبت</h1>", unsafe_allow_html=True)
    st.write(f"المكتبة محملة: {len(st.session_state.db)} كلمة")
    
    if st.button("📖 القاموس والمراجعة"): st.session_state.page = "dict"; st.rerun()
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚔️ غرفة الاختبار"): 
            st.session_state.test_q = random.choice(st.session_state.db)
            st.session_state.page = "test"; st.rerun()
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
    with c2:
        if st.button("⏳ تحدي 60 ثانية"): st.session_state.page = "blitz"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [3] غرفة الاختبار (مصلحة بالكامل)
elif st.session_state.page == "test":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    
    q = st.session_state.test_q
    st.markdown(f"### ما معنى: <span style='color:#D4AC0D;'>{q['eng']}</span>؟", unsafe_allow_html=True)
    ans = st.text_input("اكتب المعنى بالعربي:")
    
    if st.button("تحقق ✅"):
        if ans.strip() == q['ara']:
            st.success("بطل! +20 نقطة")
            st.session_state.score += 20
            st.session_state.test_q = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"خطأ! الإجابة الصحيحة: {q['ara']}")

    st.markdown('</div>', unsafe_allow_html=True)

# [4] غرفة القاموس (مستويات + نطق)
elif st.session_state.page == "dict":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    
    lvl = st.selectbox("تصفية حسب المستوى:", ["الكل", "سهل", "متوسط", "صعب"])
    search = st.text_input("🔍 ابحث عن كلمة...")
    
    filtered = [w for w in st.session_state.db if (lvl == "الكل" or w['lv'] == lvl) and (search.lower() in w['eng'].lower() or search in w['ara'])]
    
    for i, w in enumerate(filtered[:50]):
        col_t, col_s = st.columns([5, 1])
        col_t.markdown(f"<div class='word-item'><b>{w['eng']}</b> <span>{w['ara']}</span></div>", unsafe_allow_html=True)
        if col_s.button("🔊", key=f"s_{i}"):
            speak(w['eng'])
            st.session_state.read_count += 1
    st.markdown('</div>', unsafe_allow_html=True)

# [5] الملف الشخصي (ألقاب + أوسمة)
elif st.session_state.page == "profile":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h2>👤 لوحة الإنجاز</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.metric("الكلمات المسموعة", st.session_state.read_count)
    c2.metric("نقاط الخبرة", st.session_state.score)
    
    rank = "مستكشف 🌲" if st.session_state.score < 500 else "ملك الجبال 👑"
    st.markdown(f"### رتبتك الحالية: {rank}")
    
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [6] غرفة الاسترخاء (فيديو الدعاء)
elif st.session_state.page == "relax":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
