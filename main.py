import streamlit as st
import random
import time
import requests
import re

# --- 1. التصميم الزجاجي الفخم ---
st.set_page_config(page_title="Abt Academy Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; 
        background-attachment: fixed;
    }
    .glass-card {
        background: rgba(0, 0, 0, 0.8); 
        backdrop-filter: blur(15px);
        border-radius: 25px; 
        padding: 25px; 
        color: white;
        border: 1px solid rgba(255,255,255,0.1); 
        margin-bottom: 20px;
    }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1) !important; 
        color: white !important;
        border-radius: 12px !important; 
        border: 1px solid rgba(255,255,255,0.3) !important;
        height: 50px !important; 
        transition: 0.3s; 
        width: 100%;
    }
    .stButton>button:hover { 
        background: #D4AC0D !important; 
        color: black !important; 
    }
    .word-box {
        background: rgba(255,255,255,0.05); 
        padding: 15px; 
        border-radius: 15px;
        margin: 8px 0; 
        border-right: 5px solid #D4AC0D; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (جلب الكلمات) ---
@st.cache_data
def load_abt_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    data = []
    try:
        r = requests.get(url, timeout=5)
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
        if data:
            return data
    except Exception as e:
        pass
    return [{"eng": "Mountain", "ara": "جبل", "lv": "سهل"}]

# --- 3. نظام إدارة الجلسة ---
if 'db' not in st.session_state: 
    st.session_state.db = load_abt_data()
if 'page' not in st.session_state: 
    st.session_state.page = "dua"
if 'score' not in st.session_state: 
    st.session_state.score = 0
if 'words_read' not in st.session_state: 
    st.session_state.words_read = 0
if 'favs' not in st.session_state: 
    st.session_state.favs = []
if 'test_word' not in st.session_state: 
    st.session_state.test_word = random.choice(st.session_state.db)

def speak(text):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={text}&type=2")

# --- 4. تنفيذ الغرف والمشاهد ---

# [1] غرفة الدعاء (البداية)
if st.session_state.page == "dua":
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h1>✨ فاتحة طلب العلم</h1>
        <h3>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("بسم الله - دخول الأكاديمية", key="btn_dua_enter"):
        st.session_state.page = "main"
        st.rerun()

# [2] القاعة الرئيسية
elif st.session_state.page == "main":
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h1>🏔️ أكاديمية أبت الذكية</h1>
        <p>المكتبة محملة بـ <b>{len(st.session_state.db)}</b> كلمة</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress = min((st.session_state.words_read / len(st.session_state.db)) * 100, 100)
    st.write(f"نسبة الإنجاز: {progress:.1f}%")
    st.progress(progress / 100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس (مستويات وصفحات)", key="nav_dict"): 
            st.session_state.page = "dict"
            st.rerun()
        if st.button("⚔️ غرفة الاختبار", key="nav_test"): 
            st.session_state.page = "test"
            st.rerun()
    with col2:
        if st.button("👤 الملف الشخصي", key="nav_profile"): 
            st.session_state.page = "profile"
            st.rerun()
        if st.button("🌿 غرفة الاسترخاء", key="nav_relax"): 
            st.session_state.page = "relax"
            st.rerun()
    
    st.write("")
    if st.button("⭐ الكلمات المفضلة", key="nav_favs"): 
        st.session_state.page = "favs"
        st.rerun()

# [3] غرفة القاموس
elif st.session_state.page == "dict":
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_dict"): 
        st.session_state.page = "main"
        st.rerun()
        
    st.markdown('<div class="glass-card"><h1>📖 القاموس الذكي</h1></div>', unsafe_allow_html=True)
    
    level = st.radio("المستوى:", ["الكل", "سهل", "متوسط", "صعب"], horizontal=True, key="filter_level")
    search = st.text_input("🔍 بحث سريع...", key="filter_search")
    
    filtered = [
        w for w in st.session_state.db 
        if (level == "الكل" or w['lv'] == level) and 
           (search.lower() in w['eng'].lower() or search in w['ara'])
    ]
    
    if filtered:
        words_per_page = 20
        total_pages = max(1, (len(filtered) + words_per_page - 1) // words_per_page)
        
        page_num = st.number_input("الصفحة:", min_value=1, max_value=total_pages, step=1, key="dict_page_num")
        
        start_idx = (page_num - 1) * words_per_page
        end_idx = start_idx + words_per_page
        
        for i, w in enumerate(filtered[start_idx:end_idx]):
            st.markdown(f'''
            <div class="word-box">
                <div><b>{w["eng"]}</b> <small>({w["lv"]})</small></div> 
                <b>{w["ara"]}</b>
            </div>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button(f"🔊 نطق", key=f"s_{page_num}_{i}"):
                speak(w['eng'])
                st.session_state.words_read += 1
            if c2.button(f"⭐ تفضيل", key=f"f_{page_num}_{i}"):
                if w not in st.session_state.favs: 
                    st.session_state.favs.append(w)
                    st.toast(f"تمت إضافة {w['eng']} للمفضلة! ⭐")
    else:
        st.info("لا توجد نتائج تطابق بحثك.")

# [4] غرفة الاختبار
elif st.session_state.page == "test":
    if st.button("🔙 إنهاء الاختبار", key="back_from_test"): 
        st.session_state.page = "main"
        st.rerun()
        
    word = st.session_state.test_word
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h2>⚔️ اختبر معلوماتك</h2>
        <h3>ما معنى كلمة: <span style="color:#D4AC0D;">{word['eng']}</span>؟</h3>
    </div>
    """, unsafe_allow_html=True)
    
    ans = st.text_input("الإجابة باللغة العربية:", key="test_answer_input")
    
    if st.button("تحقق ✅", key="btn_check_answer"):
        if ans.strip() == word['ara']:
            st.success("إجابة صحيحة! +20 نقطة 🎉")
            st.session_state.score += 20
            st.session_state.test_word = random.choice(st.session_state.db)
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"إجابة خاطئة! المعنى الصحيح هو: **{word['ara']}**")

# [5] الملف الشخصي
elif st.session_state.page == "profile":
    rank = "مستكشف 🌲" if st.session_state.score < 500 else "فارس ⚔️" if st.session_state.score < 1500 else "إمبراطور القمة 👑"
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h1>👤 إحصائيات البطل</h1>
        <h2>الرتبة: <span style="color:#D4AC0D;">{rank}</span></h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("نقاط الاختبار", st.session_state.score)
    col2.metric("كلمات تمت مراجعتها", st.session_state.words_read)
    
    st.write("")
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_profile"): 
        st.session_state.page = "main"
        st.rerun()

# [6] غرفة الاسترخاء
elif st.session_state.page == "relax":
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h1>🌿 غرفة الاسترخاء والتركيز</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_relax"): 
        st.session_state.page = "main"
        st.rerun()

# [7] غرفة المفضلة
elif st.session_state.page == "favs":
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_favs"): 
        st.session_state.page = "main"
        st.rerun()
        
    st.markdown('<div class="glass-card"><h1>⭐ الكلمات المفضلة</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.favs:
        for idx, w in enumerate(st.session_state.favs):
            st.markdown(f'''
            <div class="word-box">
                <b>{w["eng"]}</b> 
                <b>{w["ara"]}</b>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("لم تقم بإضافة أي كلمات للمفضلة بعد.")
