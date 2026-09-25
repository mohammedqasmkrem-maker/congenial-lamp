import streamlit as st
import streamlit.components.v1 as components
import random
import time
import requests
import re

# --- 1. الإعدادات والتصميم الزجاجي ---
st.set_page_config(page_title="Abt Academy Pro", layout="wide", initial_sidebar_state="collapsed")

# دالة مخصصة لزرع رمز AdSense في الصفحة الحالية
def inject_adsense():
    adsense_code = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2272014930208509"
         crossorigin="anonymous"></script>
    """
    components.html(adsense_code, height=0)

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; 
        background-attachment: fixed;
    }
    .glass-card {
        background: rgba(15, 23, 42, 0.75); 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px; 
        padding: 30px; 
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.15); 
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important; 
        color: white !important;
        border-radius: 14px !important; 
        border: 1px solid rgba(255,255,255,0.2) !important;
        height: 52px !important; 
        font-weight: bold !important;
        transition: all 0.3s ease !important; 
        width: 100%;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #D4AC0D, #F1C40F) !important; 
        color: #000 !important; 
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 172, 13, 0.4);
    }
    
    .dict-card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 18px;
        padding: 18px 22px;
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-right: 6px solid #D4AC0D;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
    }
    .dict-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-right-color: #F1C40F;
    }
    .badge-easy { background: #27ae60; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    .badge-medium { background: #e67e22; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    .badge-hard { background: #e74c3c; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات ---
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
    except:
        pass
    return [{"eng": "Letter", "ara": "رسالة / حرف", "lv": "سهل"}]

# --- 3. نظام الجلسة ---
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

# --- 4. الشاشات والغرف (مع تضمين الرمز في كل غرفة) ---

# [1] غرفة الدعاء
if st.session_state.page == "dua":
    inject_adsense()
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h1>✨ فاتحة طلب العلم</h1>
        <h3 style="color: #D4AC0D; margin-top:20px;">اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("بسم الله - دخول الأكاديمية", key="btn_dua_enter"):
        st.session_state.page = "main"
        st.rerun()

# [2] القاعة الرئيسية
elif st.session_state.page == "main":
    inject_adsense()
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h1>🏔️ أكاديمية أبت الذكية</h1>
        <p style="font-size: 18px;">المكتبة محملة بـ <b style="color:#D4AC0D;">{len(st.session_state.db)}</b> كلمة احترافية</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress = min((st.session_state.words_read / len(st.session_state.db)) * 100, 100)
    st.write(f"📊 نسبة الإنجاز: **{progress:.1f}%**")
    st.progress(progress / 100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس الفخم", key="nav_dict"): 
            st.session_state.page = "dict"
            st.rerun()
        if st.button("⚔️ غرفة الاختبار الذكية", key="nav_test"): 
            st.session_state.page = "test"
            st.rerun()
    with col2:
        if st.button("👤 الملف الشخصي والإحصائيات", key="nav_profile"): 
            st.session_state.page = "profile"
            st.rerun()
        if st.button("🌿 غرفة الاسترخاء", key="nav_relax"): 
            st.session_state.page = "relax"
            st.rerun()
    
    st.write("")
    if st.button(f"⭐ الكلمات المفضلة ({len(st.session_state.favs)})", key="nav_favs"): 
        st.session_state.page = "favs"
        st.rerun()

# [3] غرفة القاموس
elif st.session_state.page == "dict":
    inject_adsense()
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_dict"): 
        st.session_state.page = "main"
        st.rerun()
        
    st.markdown('<div class="glass-card"><h1>📖 القاموس التفاعلي الحديث</h1></div>', unsafe_allow_html=True)
    
    c_filt1, c_filt2 = st.columns([1, 2])
    with c_filt1:
        level = st.radio("فلترة المستوى:", ["الكل", "سهل", "متوسط", "صعب"], horizontal=True, key="filter_level")
    with c_filt2:
        search = st.text_input("🔍 بحث سريع عن كلمة...", key="filter_search")
    
    filtered = [
        w for w in st.session_state.db 
        if (level == "الكل" or w['lv'] == level) and 
           (search.lower() in w['eng'].lower() or search in w['ara'])
    ]
    
    if filtered:
        words_per_page = 15
        total_pages = max(1, (len(filtered) + words_per_page - 1) // words_per_page)
        
        page_num = st.number_input("الصفحة:", min_value=1, max_value=total_pages, step=1, key="dict_page_num")
        start_idx = (page_num - 1) * words_per_page
        end_idx = start_idx + words_per_page
        
        for i, w in enumerate(filtered[start_idx:end_idx]):
            badge_class = "badge-easy" if w["lv"] == "سهل" else "badge-medium" if w["lv"] == "متوسط" else "badge-hard"
            
            st.markdown(f'''
            <div class="dict-card">
                <div>
                    <span style="font-size: 22px; font-weight: bold; color: #fff;">{w["eng"]}</span>
                    <span class="{badge_class}" style="margin-right: 10px;">{w["lv"]}</span>
                </div>
                <div style="font-size: 20px; font-weight: bold; color: #D4AC0D;">
                    {w["ara"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button(f"🔊 استماع للنطق", key=f"s_{page_num}_{i}"):
                speak(w['eng'])
                st.session_state.words_read += 1
            if c2.button(f"⭐ إضافة للمفضلة", key=f"f_{page_num}_{i}"):
                if w not in st.session_state.favs: 
                    st.session_state.favs.append(w)
                    st.toast(f"تمت إضافة ({w['eng']}) إلى المفضلة! ⭐")
    else:
        st.info("لا توجد نتائج تطابق بحثك.")

# [4] غرفة الاختبار الذكية
elif st.session_state.page == "test":
    inject_adsense()
    if st.button("🔙 إنهاء الاختبار", key="back_from_test"): 
        st.session_state.page = "main"
        st.rerun()
        
    word = st.session_state.test_word
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h2>⚔️ اختبر معلوماتك</h2>
        <h3 style="margin-top:20px;">ما معنى كلمة: <span style="color:#D4AC0D; font-size:36px;">{word['eng']}</span>؟</h3>
    </div>
    """, unsafe_allow_html=True)
    
    ans = st.text_input("الإجابة باللغة العربية:", key="test_answer_input")
    
    col_ans1, col_ans2 = st.columns(2)
    with col_ans1:
        if st.button("تحقق ✅", key="btn_check_answer"):
            user_input = ans.strip().lower()
            
            possible_meanings = [m.strip().lower() for m in re.split(r'[/،,-]', word['ara'])]
            
            if user_input == word['eng'].strip().lower() or user_input in possible_meanings:
                st.success("إجابة صحيحة! +20 نقطة 🎉")
                st.session_state.score += 20
                st.session_state.test_word = random.choice(st.session_state.db)
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"إجابة خاطئة! المعنى الصحيح هو: **{word['ara']}**")

    with col_ans2:
        if st.button("🔊 استماع للنطق", key="btn_listen_test"):
            speak(word['eng'])

# [5] الملف الشخصي
elif st.session_state.page == "profile":
    inject_adsense()
    rank = "مستكشف 🌲" if st.session_state.score < 500 else "فارس ⚔️" if st.session_state.score < 1500 else "إمبراطور القمة 👑"
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h1>👤 إحصائياتك ورتبتك</h1>
        <h2 style="color:#D4AC0D; margin-top:15px;">رتبتك الحالية: {rank}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("إجمالي نقاط الاختبار", st.session_state.score)
    col2.metric("عدد الكلمات المراجعة", st.session_state.words_read)
    
    st.write("")
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_profile"): 
        st.session_state.page = "main"
        st.rerun()

# [6] غرفة الاسترخاء
elif st.session_state.page == "relax":
    inject_adsense()
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
    inject_adsense()
    if st.button("🔙 عودة للقاعة الرئيسية", key="back_from_favs"): 
        st.session_state.page = "main"
        st.rerun()
        
    st.markdown('<div class="glass-card"><h1>⭐ الكلمات المفضلة المحفوظة</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.favs:
        for idx, w in enumerate(st.session_state.favs):
            st.markdown(f'''
            <div class="dict-card">
                <span style="font-size: 20px; font-weight: bold; color: #fff;">{w["eng"]}</span>
                <span style="font-size: 20px; font-weight: bold; color: #D4AC0D;">{w["ara"]}</span>
            </div>
            ''', unsafe_allow_html=True)
            if st.button(f"🔊 نطق {w['eng']}", key=f"fav_spk_{idx}"):
                speak(w['eng'])
    else:
        st.info("لم تقم بإضافة أي كلمات للمفضلة بعد.")
                 
