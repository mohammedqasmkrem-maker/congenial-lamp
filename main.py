import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية والفخامة ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 25, 20, 0.98); z-index: -1;
    }
    .royal-card {
        background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D;
        border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px; color: white;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; font-family: 'serif'; }
    .stat-box { font-size: 20px; color: #D4AC0D; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (vocab.csv) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Success", "Arabic": "نجاح"}]

# --- 3. تهيئة الملف الشخصي والنظام (بيانات حقيقية) ---
if 'db' not in st.session_state: st.session_state.db = load_data()
if 'score' not in st.session_state: st.session_state.score = 0
if 'words_count' not in st.session_state: st.session_state.words_count = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def get_rank(s):
    if s < 500: return "طالب علم 🌱"
    if s < 2000: return "فارس الحروف ⚔️"
    return "الملك الأبتي 👑"

# --- 4. نظام الغرف الملكية ---

# الغرفة (1): دعاء طلب العلم
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:26px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر الملكي", use_container_width=True):
        st.session_state.page = "hall"
        st.rerun()

# الغرفة (2): القاعة الرئيسية
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='royal-card'><h3>👤 الملف الشخصي</h3><p>عرض مستواك ونقاطك الحقيقية</p></div>", unsafe_allow_html=True)
        if st.button("دخول الملف الشخصي", use_container_width=True): st.session_state.page = "profile"

        st.markdown("<div class='royal-card'><h3>⏳ تحدي 60 ثانية</h3><p>اختبار ذكاء سريع ضد الوقت</p></div>", unsafe_allow_html=True)
        if st.button("بدء التحدي السريع", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.page = "blitz"

    with col2:
        st.markdown("<div class='royal-card'><h3>🛠️ تكوين الجمل</h3><p>بناء جمل إنجليزية ذكية</p></div>", unsafe_allow_html=True)
        if st.button("بدء بناء الجمل", use_container_width=True): st.session_state.page = "sentences"

        st.markdown("<div class='royal-card'><h3>🌿 غرفة الاسترخاء</h3><p>هدوء، طبيعة، وتركيز</p></div>", unsafe_allow_html=True)
        if st.button("دخول غرفة الاسترخاء", use_container_width=True): st.session_state.page = "relax"

# الغرفة (3): الملف الشخصي (حقيقي)
elif st.session_state.page == "profile":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>👤 بياناتك الملكية</h1></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='royal-card'><h3>الرتبة</h3><p class='stat-box'>{get_rank(st.session_state.score)}</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='royal-card'><h3>النقاط</h3><p class='stat-box'>{st.session_state.score}</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='royal-card'><h3>كلمات</h3><p class='stat-box'>{st.session_state.words_count}</p></div>", unsafe_allow_html=True)
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()

# الغرفة (4): غرفة الاسترخاء
elif st.session_state.page == "relax":
    st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 لحظة هدوء</h2></div>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()

# الغرفة (5): تحدي الـ 60 ثانية (ذكاء)
elif st.session_state.page == "blitz":
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("رجوع", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h2 style='color:red; text-align:center;'>⏳ {rem} ثانية</h2>", unsafe_allow_html=True)
        if 'word' not in st.session_state or st.session_state.get('new_word', True):
            st.session_state.word = random.choice(st.session_state.db)
            st.session_state.new_word = False
        
        st.write(f"ترجم بسرعة: **{st.session_state.word['English']}**")
        ans = st.text_input("الإجابة:", key="speed_in")
        if st.button("تحقق ✅"):
            if ans.strip() == st.session_state.word['Arabic']:
                st.session_state.score += 60
                st.session_state.words_count += 1
                st.session_state.new_word = True
                st.rerun()

# الغرفة (6): تكوين الجمل
elif st.session_state.page == "sentences":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    if 's_word' not in st.session_state: st.session_state.s_word = random.choice(st.session_state.db)
    word = st.session_state.s_word
    st.markdown(f"<div class='royal-card'><h3>The __ is essential for us.</h3><p>المطلوب وضع كلمة: {word['Arabic']}</p></div>", unsafe_allow_html=True)
    user_word = st.text_input("اكتب الكلمة بالإنجليزية:")
    if st.button("بناء ✅"):
        if user_word.lower().strip() == word['English'].lower():
            st.success("بطل! +20 نقطة")
            st.session_state.score += 20
            st.session_state.s_word = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        
