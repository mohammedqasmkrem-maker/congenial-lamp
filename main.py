import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم الزجاجي المتطور (Glassmorphism 2.0) ---
st.set_page_config(page_title="Abt Academy Ultimate", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .glass-room {
        background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 35px; color: white; text-align: center;
        max-width: 950px; margin: auto; box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }
    .stButton>button {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
        color: white !important; border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 15px !important; height: 60px !important; font-size: 18px !important;
        transition: 0.4s; width: 100%;
    }
    .stButton>button:hover {
        background: rgba(255,255,255,0.3) !important; border: 1px solid white !important;
        transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    .word-card {
        background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px;
        margin: 10px 0; border-left: 5px solid #D4AC0D; display: flex;
        justify-content: space-between; align-items: center; backdrop-filter: blur(5px);
    }
    .progress-bar { width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 10px; margin: 10px 0; }
    .progress-fill { height: 10px; background: #D4AC0D; border-radius: 10px; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات الذكي (تحميل الـ 1011 كلمة) ---
@st.cache_data
def load_all_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            words = []
            for line in r.text.splitlines():
                if " - " in line:
                    p = line.split(" - ")
                    eng = re.sub(r'[^a-zA-Z\s]', '', p[0]).strip()
                    ara = p[1].strip()
                    if eng and ara:
                        lv = "🟢 سهل" if len(eng) <= 4 else "🟡 متوسط" if len(eng) <= 7 else "🔴 صعب"
                        words.append({"eng": eng, "ara": ara, "lv": lv})
            return words
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "🟢 سهل"}]

# --- 3. نظام الجلسة المتكامل (المميزات الـ 20) ---
if 'db' not in st.session_state: st.session_state.db = load_all_data()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'words_heard' not in st.session_state: st.session_state.words_heard = set()
if 'correct_tests' not in st.session_state: st.session_state.correct_tests = 0
if 'favorites' not in st.session_state: st.session_state.favorites = []

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

def get_rank():
    s = st.session_state.score
    if s >= 2000: return "👑 إمبراطور القمة", "🏆 وسام الذهب"
    if s >= 1000: return "⚔️ بطل الأكاديمية", "🥇 وسام الفضة"
    return "🌲 مستكشف الجبال", "🥉 وسام البداية"

# --- 4. تنفيذ الغرف الذكية ---

# [غرفة 1] بوابة الدعاء
if st.session_state.page == "dua":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:45px;'>✨ فاتحة العلم</h1>", unsafe_allow_html=True)
    st.write("### اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
    if st.button("دخول الأكاديمية (بسم الله)"):
        st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [غرفة 2] القاعة الرئيسية
elif st.session_state.page == "hall":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    rank, badge = get_rank()
    st.markdown(f"<h1>🏔️ {rank}</h1>", unsafe_allow_html=True)
    
    # شريط التقدم العام
    progress = (len(st.session_state.words_heard) / len(st.session_state.db)) * 100
    st.markdown(f"**تقدمك في حفظ الـ 1011 كلمة: {progress:.1f}%**", unsafe_allow_html=True)
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress}%;"></div></div>', unsafe_allow_html=True)

    if st.button("📖 القاموس الذكي (المستويات)"): st.session_state.page = "dict"; st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ غرفة الاختبار"): 
            st.session_state.t_q = random.choice(st.session_state.db); st.session_state.page = "test"; st.rerun()
        if st.button("👤 ملف الإنجازات"): st.session_state.page = "profile"; st.rerun()
    with col2:
        if st.button("⭐ كلماتي المفضلة"): st.session_state.page = "favs"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [غرفة 3] القاموس (بحث + نطق + مستويات + تفضيل)
elif st.session_state.page == "dict":
    st.markdown('<div class="glass-room" style="max-width:1100px;">', unsafe_allow_html=True)
    if st.button("🔙 العودة للمدخل"): st.session_state.page = "hall"; st.rerun()
    
    lv_filter = st.selectbox("اختر المستوى:", ["الكل", "🟢 سهل", "🟡 متوسط", "🔴 صعب"])
    search = st.text_input("🔍 ابحث عن كلمة...")
    
    filtered = [w for w in st.session_state.db if (lv_filter == "الكل" or w['lv'] == lv_filter) and (search.lower() in w['eng'].lower() or search in w['ara'])]
    
    for i, w in enumerate(filtered[:40]):
        with st.container():
            st.markdown(f'<div class="word-card"><div><b>{w["eng"]}</b><br><small>{w["lv"]}</small></div> <b>{w["ara"]}</b></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1,1,1])
            if c1.button(f"🔊 نطق", key=f"v_{i}"):
                speak(w['eng']); st.session_state.words_heard.add(w['eng'])
            if c2.button(f"⭐ تفضيل", key=f"f_{i}"):
                if w not in st.session_state.favorites: st.session_state.favorites.append(w)
    st.markdown('</div>', unsafe_allow_html=True)

# [غرفة 4] الملف الشخصي (إحصائيات + ألقاب)
elif st.session_state.page == "profile":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    rank, badge = get_rank()
    st.markdown(f"<h2>👤 {rank}</h2><h3>{badge}</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("كلمات سمعتها", len(st.session_state.words_heard))
    c2.metric("اختبارات ناجحة", st.session_state.correct_tests)
    c3.metric("مجموع النقاط", st.session_state.score)
    
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [غرفة 5] غرفة الاختبار (التعلم النشط)
elif st.session_state.page == "test":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    if st.button("🔙 إنهاء الاختبار"): st.session_state.page = "hall"; st.rerun()
    
    q = st.session_state.t_q
    st.markdown(f"### ما ترجمة: <h1 style='color:#D4AC0D;'>{q['eng']}</h1>", unsafe_allow_html=True)
    ans = st.text_input("الإجابة:")
    if st.button("تحقق ✅"):
        if ans.strip() == q['ara']:
            st.success("بطل! إجابة دقيقة (+20 نقطة)"); st.session_state.score += 20
            st.session_state.correct_tests += 1; st.session_state.t_q = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else: st.error(f"خطأ! الصحيح هو: {q['ara']}")
    st.markdown('</div>', unsafe_allow_html=True)

# [غرفة 6] غرفة الاسترخاء
elif st.session_state.page == "relax":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [غرفة 7] المفضلة
elif st.session_state.page == "favs":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown("## ⭐ كلماتك المختارة")
    for w in st.session_state.favorites:
        st.markdown(f'<div class="word-card"><b>{w["eng"]}</b> <b>{w["ara"]}</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
                
