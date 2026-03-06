import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم الزجاجي (Glassmorphism) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    /* تثبيت صورة الجبال بالخلفية */
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* الغرف الزجاجية - تأثير Frosted Glass */
    .glass-room {
        background: rgba(0, 0, 0, 0.75); 
        backdrop-filter: blur(15px); /* تأثير التغبيش الزجاجي */
        padding: 40px; 
        border-radius: 35px;
        border: 2px solid rgba(212, 172, 13, 0.5); 
        color: white;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        margin: 20px auto;
        max-width: 800px;
    }

    /* كروت القاموس - زجاج فاتح */
    .word-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        border-left: 10px solid #D4AC0D;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(5px);
    }

    /* أزرار القصر الملكية */
    .stButton>button {
        background: linear-gradient(135deg, #D4AC0D 0%, #B8860B 100%) !important;
        color: black !important;
        font-weight: 900 !important;
        height: 70px !important;
        border-radius: 20px !important;
        font-size: 22px !important;
        border: none !important;
        transition: 0.3s ease-in-out;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 25px rgba(212, 172, 13, 0.4) !important;
    }

    /* الملف الشخصي - لوحة الإنجاز */
    .stat-box {
        background: rgba(212, 172, 13, 0.2);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid #D4AC0D;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (الربط مع الـ 1011 كلمة) ---
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
                    eng = re.sub(r'[^a-zA-Z\s]', '', p[0]).strip()
                    ara = p[1].strip()
                    if eng and ara:
                        lv = "🟢 سهل" if len(eng) <= 4 else "🟡 متوسط" if len(eng) <= 7 else "🔴 صعب"
                        data.append({"eng": eng, "ara": ara, "lv": lv})
        return data
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "🟢 سهل"}]

# --- 3. تهيئة الجلسة ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'read_count' not in st.session_state: st.session_state.read_count = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def get_rank():
    s = st.session_state.score
    if s >= 2000: return "👑 إمبراطور القمة", "🏆 وسام الذهب الملكي"
    if s >= 1000: return "⚔️ جنرال الأكاديمية", "🥇 وسام الشجاعة الفضي"
    if s >= 500: return "🛡️ فارس الجبال", "🥈 وسام النحاس"
    return "🌲 مستكشف مبتدئ", "🥉 وسام البداية"

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. نظام الغرف الملكية ---

# -- غرفة الدعاء --
if st.session_state.page == "dua":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#D4AC0D; font-size:50px;'>✨ فاتحة العلم</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:26px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
    if st.button("آمين - دخول الإمبراطورية"):
        st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -- المدخل الرئيسي (القصر) --
elif st.session_state.page == "hall":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#D4AC0D; font-size:45px;'>🏔️ قصر Abt الملكي</h1>", unsafe_allow_html=True)
    st.write(f"المكتبة محملة بـ **{len(st.session_state.db)}** كلمة مصنفة ✅")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📖 غرفة القاموس (المستويات)"): st.session_state.page = "dict"; st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        if st.button("⚔️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
    with col2:
        if st.button("⏳ تحدي 60 ثانية"): 
            st.session_state.start_t = time.time()
            st.session_state.q = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -- غرفة القاموس --
elif st.session_state.page == "dict":
    st.markdown('<div class="glass-room" style="max-width:1000px;">', unsafe_allow_html=True)
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 style='color:#D4AC0D;'>📖 القاموس المصنف</h2>", unsafe_allow_html=True)
    
    choice = st.radio("اختر مستوى الصعوبة:", ["الكل", "🟢 سهل", "🟡 متوسط", "🔴 صعب"], horizontal=True)
    search = st.text_input("🔍 ابحث عن كلمة...")
    
    filtered = [w for w in st.session_state.db if (choice == "الكل" or w['lv'] == choice) and (search.lower() in w['eng'].lower() or search in w['ara'])]
    
    for i, w in enumerate(filtered[:100]):
        st.markdown(f"""
        <div class="word-card">
            <div style="text-align:left;">
                <span style="font-size:24px; font-weight:bold;">{w['eng']}</span><br>
                <small style="color:#D4AC0D;">{w['lv']}</small>
            </div>
            <div style="font-size:28px; font-weight:bold; color:#D4AC0D;">{w['ara']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"🔊 اسمع النطق", key=f"v_{i}"):
            speak(w['eng'])
            st.session_state.read_count += 1
    st.markdown('</div>', unsafe_allow_html=True)

# -- غرفة الملف الشخصي --
elif st.session_state.page == "profile":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    rank, badge = get_rank()
    st.markdown(f"<h1 style='color:#D4AC0D;'>👤 ملف البطل</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='background:rgba(212,172,13,0.2); border-radius:15px; padding:10px;'>{rank}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>🏅 {badge}</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='stat-box'>📖 كلمات قرأتها<br><h1>{st.session_state.read_count}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-box'>💰 مجموع النقاط<br><h1>{st.session_state.score}</h1></div>", unsafe_allow_html=True)
    
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -- غرفة الاختبار --
elif st.session_state.page == "test":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(st.session_state.db)
    tq = st.session_state.t_q
    st.markdown(f"### ترجم الكلمة إلى العربية:<br><h1 style='color:#D4AC0D; font-size:60px;'>{tq['eng']}</h1>", unsafe_allow_html=True)
    ans = st.text_input("أدخل الإجابة:")
    if st.button("تحقق من صحة الإجابة ✅"):
        if ans.strip() == tq['ara']:
            st.success("إجابة إمبراطورية! +20 نقطة")
            st.session_state.score += 20
            st.session_state.t_q = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else: st.error("حاول مرة أخرى يا بطل")
    st.markdown('</div>', unsafe_allow_html=True)

# -- غرفة الاسترخاء --
elif st.session_state.page == "relax":
    st.markdown('<div class="glass-room">', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
                
