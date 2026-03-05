import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية (تثبيت الخلفية) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.97); z-index: -1; }
    .royal-card { background: rgba(20, 35, 30, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px; color: white; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. جلب الكلمات من vocab.csv (الربط المباشر) ---
@st.cache_data
def load_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv" #
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True) #
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Time", "Arabic": "الوقت"}]

# --- 3. تهيئة الحالة (حل مشكلة التطبيق الفارغ) ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'page' not in st.session_state: st.session_state.page = "hall"
if 'db' not in st.session_state: st.session_state.db = load_vocab()
if 'show_dua' not in st.session_state: st.session_state.show_dua = True

# --- 4. نافذة الدعاء (أول ما تفتح التطبيق) ---
if st.session_state.show_dua:
    st.markdown("<div class='royal-card'><h2 class='gold-text'>✨ دعاء طلب العلم</h2><p>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول الأكاديمية", use_container_width=True):
        st.session_state.show_dua = False
        st.rerun()

# --- 5. الواجهة الرئيسية (القصر) ---
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='royal-card'><h2 class='gold-text'>👤 الملف الشخصي</h2><p>نقاطك: {st.session_state.score} | الـ Streak: {st.session_state.streak}</p></div>", unsafe_allow_html=True)
        if st.button("📖 القاموس الشامل", use_container_width=True): st.session_state.page = "dictionary"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>⏳ تحدي الـ 60 ثانية</h2><p>تكوين جمل ذكي ضد الوقت</p></div>", unsafe_allow_html=True)
        if st.button("⚔️ بدء التحدي (60 نقطة)", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.current_word = random.choice(st.session_state.db)
            st.session_state.page = "blitz"
            st.rerun()

    st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 الطبيعة الحلال</h2></div>", unsafe_allow_html=True)
    if st.button("🧘 دخول غرفة الاسترخاء", use_container_width=True): st.session_state.page = "nature"

    st.markdown(f"<p style='text-align:center;'><a href='https://share.streamlit.io/user/mqasmkrem-a11y' style='color:#D4AC0D; text-decoration:none;'>🔗 الرابط الرسمي للمنصة</a></p>", unsafe_allow_html=True)

# --- 6. القاموس (Dictionary) ---
elif st.session_state.page == "dictionary":
    st.markdown("<h2 class='gold-text'>📖 قاموس الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    search = st.text_input("🔍 ابحث عن كلمة...")
    for i, w in enumerate(st.session_state.db[:100]): # عرض أول 100 لسرعة التصفح
        if search.lower() in w['English'].lower():
            st.write(f"**{w['English']}** : {w['Arabic']}")

# --- 7. تحدي الـ 60 ثانية (التحدي الذكي) ---
elif st.session_state.page == "blitz":
    remaining = 60 - int(time.time() - st.session_state.start_time)
    if remaining <= 0:
        st.warning("💥 انتهى الوقت!")
        if st.button("العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    else:
        st.markdown(f"<h2 style='color:red;'>⏳ {remaining} ثانية</h2>", unsafe_allow_html=True)
        word = st.session_state.current_word
        st.markdown(f"<div class='royal-card'><h3>I need to find the __.</h3><p>الترجمة: {word['Arabic']}</p></div>", unsafe_allow_html=True)
        ans = st.text_input("اكتب الكلمة الناقصة:").strip().lower()
        if st.button("تحقق ✅"):
            if ans == word['English'].lower():
                st.session_state.score += 60
                st.session_state.current_word = random.choice(st.session_state.db)
                st.rerun()

# --- 8. الفيديو (الطبيعة) ---
elif st.session_state.page == "nature":
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.video("https://youtu.be/0wt-HbRw_pw?si=IJ23Q_Mcbb07Kdny")
    
