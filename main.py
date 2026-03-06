import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم الزجاجي الفخم (20 ميزة تصميمية) ---
st.set_page_config(page_title="Abt Academy Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .glass-card {
        background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(15px);
        border-radius: 25px; padding: 25px; color: white;
        border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;
    }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1) !important; color: white !important;
        border-radius: 12px !important; border: 1px solid rgba(255,255,255,0.3) !important;
        height: 50px !important; transition: 0.3s; width: 100%;
    }
    .stButton>button:hover { background: #D4AC0D !important; color: black !important; }
    .word-box {
        background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px;
        margin: 8px 0; border-right: 5px solid #D4AC0D; display: flex; 
        justify-content: space-between; align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (جلب الـ 1011 كلمة) ---
@st.cache_data
def load_abt_data():
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
                        lv = "سهل" if len(eng) <= 4 else "متوسط" if len(eng) <= 7 else "صعب"
                        data.append({"eng": eng, "ara": ara, "lv": lv})
        return data
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "سهل"}]

# --- 3. نظام إدارة الجلسة (المميزات الـ 20) ---
if 'db' not in st.session_state: st.session_state.db = load_abt_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'words_read' not in st.session_state: st.session_state.words_read = 0
if 'favs' not in st.session_state: st.session_state.favs = []
if 'test_word' not in st.session_state: st.session_state.test_word = random.choice(st.session_state.db)

def speak(text):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={text}&type=2")

# --- 4. تنفيذ الغرف (بناءً على طلبك) ---

# [1] غرفة الدعاء (البداية)
if st.session_state.page == "dua":
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    st.title("✨ فاتحة طلب العلم")
    st.write("### اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
    if st.button("بسم الله - دخول الأكاديمية"):
        st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [2] القاعة الرئيسية
elif st.session_state.page == "main":
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    st.title("🏔️ أكاديمية أبت الذكية")
    st.write(f"المكتبة محملة بـ **{len(st.session_state.db)}** كلمة")
    
    # شريط التقدم (Progress Bar)
    progress = min((st.session_state.words_read / len(st.session_state.db)) * 100, 100)
    st.write(f"نسبة الإنجاز: {progress:.1f}%")
    st.progress(progress / 100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس (مستويات وصفحات)"): st.session_state.page = "dict"; st.rerun()
        if st.button("⚔️ غرفة الاختبار"): st.session_state.page = "test"; st.rerun()
    with col2:
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
    
    if st.button("⭐ الكلمات المفضلة"): st.session_state.page = "favs"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [3] غرفة القاموس (مستويات + صفحات لمنع التعليق)
elif st.session_state.page == "dict":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    st.title("📖 القاموس الذكي")
    
    # فلتر المستويات
    level = st.radio("المستوى:", ["الكل", "سهل", "متوسط", "صعب"], horizontal=True)
    search = st.text_input("🔍 بحث سريح...")
    
    filtered = [w for w in st.session_state.db if (level == "الكل" or w['lv'] == level) and (search.lower() in w['eng'].lower() or search in w['ara'])]
    
    # نظام الصفحات (Pagination) - كل صفحة 20 كلمة
    words_per_page = 20
    total_pages = (len(filtered) // words_per_page) + 1
    page_num = st.number_input("الصفحة:", min_value=1, max_value=total_pages, step=1)
    
    start_idx = (page_num - 1) * words_per_page
    end_idx = start_idx + words_per_page
    
    for i, w in enumerate(filtered[start_idx:end_idx]):
        st.markdown(f'<div class="word-box"><div><b>{w["eng"]}</b> <small>({w["lv"]})</small></div> <b>{w["ara"]}</b></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button(f"🔊 نطق", key=f"s_{i}"):
            speak(w['eng']); st.session_state.words_read += 1
        if c2.button(f"⭐ تفضيل", key=f"f_{i}"):
            if w not in st.session_state.favs: st.session_state.favs.append(w)
    st.markdown('</div>', unsafe_allow_html=True)

# [4] غرفة الاختبار (مصلحة بالكامل)
elif st.session_state.page == "test":
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    if st.button("🔙 إنهاء"): st.session_state.page = "main"; st.rerun()
    
    word = st.session_state.test_word
    st.write(f"### ما معنى كلمة: # {word['eng']}")
    ans = st.text_input("الإجابة:")
    if st.button("تحقق ✅"):
        if ans.strip() == word['ara']:
            st.success("إجابة صحيحة! +20 نقطة")
            st.session_state.score += 20
            st.session_state.test_word = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"خطأ! الصحيح: {word['ara']}")
    st.markdown('</div>', unsafe_allow_html=True)

# [5] الملف الشخصي (الألقاب والجوائز)
elif st.session_state.page == "profile":
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    st.title("👤 إحصائيات البطل")
    rank = "مستكشف 🌲" if st.session_state.score < 500 else "فارس ⚔️" if st.session_state.score < 1500 else "إمبراطور القمة 👑"
    st.write(f"## الرتبة: {rank}")
    st.metric("نقاط الاختبار", st.session_state.score)
    st.metric("كلمات تمت مراجعتها", st.session_state.words_read)
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [6] غرفة الاسترخاء (فيديو)
elif st.session_state.page == "relax":
    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 عودة"): st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [7] غرفة المفضلة
elif st.session_state.page == "favs":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.title("⭐ كلماتك المفضلة")
    for w in st.session_state.favs:
        st.markdown(f'<div class="word-box"><b>{w["eng"]}</b> <b>{w["ara"]}</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
