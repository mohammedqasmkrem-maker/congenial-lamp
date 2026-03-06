import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم الزجاجي العصري (Modern Glass) ---
st.set_page_config(page_title="Abt Academy", layout="wide")

st.markdown("""
    <style>
    /* صورة الجبال كخلفية ثابتة */
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* تصميم الغرفة الزجاجية الشفافة */
    .glass-box {
        background: rgba(255, 255, 255, 0.1); 
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 40px;
        color: white;
        text-align: center;
        max-width: 850px;
        margin: auto;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* أزرار عصرية بلمسة زجاجية */
    .stButton>button {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        width: 100%;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.4) !important;
        border: 1px solid white !important;
        transform: translateY(-5px);
    }

    /* كروت الكلمات */
    .word-card {
        background: rgba(0, 0, 0, 0.3);
        padding: 20px;
        border-radius: 20px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الكلمات (رابط ملفك الشخصي) ---
@st.cache_data
def get_my_vocab():
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

# --- 3. إدارة الجلسة ---
if 'db' not in st.session_state: st.session_state.db = get_my_vocab()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'read_count' not in st.session_state: st.session_state.read_count = 0

def speak(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. تنفيذ الغرف المنفصلة ---

# الغرفة 1: دعاء البداية (تظهر أول شيء)
if st.session_state.page == "dua":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:40px;'>✨ فاتحة العلم</h1>", unsafe_allow_html=True)
    st.write("### اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("دخول الأكاديمية"):
        st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الغرفة 2: القصر (المدخل الرئيسي)
elif st.session_state.page == "hall":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<h1>🏔️ أكاديمية أبت الحديثة</h1>", unsafe_allow_html=True)
    st.write(f"المكتبة: {len(st.session_state.db)} كلمة")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📖 غرفة القاموس والمراجعة"): st.session_state.page = "dict"; st.rerun()
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
        if st.button("⚔️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
    with c2:
        if st.button("⏳ تحدي الوقت"): 
            st.session_state.start_t = time.time()
            st.session_state.q = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الغرفة 3: غرفة الاسترخاء
elif st.session_state.page == "relax":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<h3>🌿 لحظة هدوء</h3>", unsafe_allow_html=True)
    # فيديو استرخاء هادئ
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الغرفة 4: القاموس
elif st.session_state.page == "dict":
    st.markdown('<div class="glass-box" style="max-width:1100px;">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2>📖 قاموس الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    
    lvl = st.radio("المستوى:", ["الكل", "سهل", "متوسط", "صعب"], horizontal=True)
    search = st.text_input("🔍 ابحث:")
    
    filtered = [w for w in st.session_state.db if (lvl == "الكل" or w['lv'] == lvl) and (search.lower() in w['eng'].lower() or search in w['ara'])]
    
    for i, w in enumerate(filtered[:50]):
        st.markdown(f"""
        <div class="word-card">
            <div style="text-align:left;"><b>{w['eng']}</b> <small>({w['lv']})</small></div>
            <div style="font-size:22px;">{w['ara']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"🔊 نطق", key=f"v_{i}"):
            speak(w['eng'])
            st.session_state.read_count += 1
    st.markdown('</div>', unsafe_allow_html=True)

# الغرفة 5: الملف الشخصي
elif st.session_state.page == "profile":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<h2>👤 لوحة الإنجازات</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: st.write(f"### 📖 كلمات قرأتها\n# {st.session_state.read_count}")
    with c2: st.write(f"### 💰 نقاطك\n# {st.session_state.score}")
    
    st.markdown("---")
    rank = "مستكشف الجبال 🌲" if st.session_state.score < 500 else "بطل الأكاديمية ⚔️"
    st.write(f"### رتبتك الحالية: {rank}")
    
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الغرفة 6: الاختبار
elif st.session_state.page == "test":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(st.session_state.db)
    tq = st.session_state.t_q
    st.markdown(f"### ما معنى كلمة: <br><h1 style='color:white;'>{tq['eng']}</h1>", unsafe_allow_html=True)
    ans = st.text_input("الإجابة:")
    if st.button("تحقق ✅"):
        if ans.strip() == tq['ara']:
            st.success("صح! +20 نقطة")
            st.session_state.score += 20; st.session_state.t_q = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else: st.error("خطأ")
    st.markdown('</div>', unsafe_allow_html=True)
                        
