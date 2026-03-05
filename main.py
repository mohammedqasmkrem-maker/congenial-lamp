import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 25, 20, 0.97); z-index: -1;
    }
    .royal-card {
        background: rgba(20, 35, 30, 0.95); border: 2px solid #D4AC0D;
        border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. جلب الكلمات من GitHub (ملف vocab.csv) ---
@st.cache_data
def load_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة الملف وتنظيفه (1011 سطر)
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Time", "Arabic": "الوقت"}]

# --- 3. تهيئة النظام (حل مشكلة AttributeError) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'page' not in st.session_state:
    st.session_state.page = "hall"
if 'db' not in st.session_state:
    st.session_state.db = load_vocab()
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.db)

# --- 4. نافذة الدعاء الملكية ---
if 'show_dua' not in st.session_state:
    st.session_state.show_dua = True

if st.session_state.show_dua:
    st.markdown("""<div style='background:#0a1a10; padding:30px; border:2px solid #D4AC0D; border-radius:15px; text-align:center;'>
    <h2 class='gold-text'>✨ دعاء طلب العلم</h2>
    <p style='color:white; font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("آمين - دخول الأكاديمية"):
        st.session_state.show_dua = False
        st.rerun()

# --- 5. الواجهة الرئيسية (نظام الغرف) ---
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='royal-card'><h2 class='gold-text'>👤 الملف الشخصي</h2><p>نقاطك: {st.session_state.score} | الـ Streak: {st.session_state.streak}</p></div>", unsafe_allow_html=True)
        if st.button("فتـح السجـل 🎖️", use_container_width=True): st.session_state.page = "profile"

        # هذا هو القاموس اللي سألت عليه
        st.markdown("<div class='royal-card'><h2 class='gold-text'>📖 القاموس الملكي</h2><p>استعرض الـ 1011 كلمة كاملة</p></div>", unsafe_allow_html=True)
        if st.button("فتح القاموس 📚", use_container_width=True): st.session_state.page = "dictionary"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>✍️ تحدي الكلمات</h2><p>اختبر كلماتك من ملف vocab.csv</p></div>", unsafe_allow_html=True)
        if st.button("بدء التحدي ⚔️", use_container_width=True): st.session_state.page = "game"

        st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 الطبيعة الحلال</h2><p>فيديو الاسترخاء والتركيز</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة 🧘", use_container_width=True): st.session_state.page = "nature"

# --- 6. صفحة القاموس (Dictionary) ---
elif st.session_state.page == "dictionary":
    st.markdown("<h2 class='gold-text' style='text-align:center;'>📖 قاموس الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    
    search = st.text_input("🔍 ابحث عن كلمة إنجليزية أو عربية:").lower()
    
    for i, w in enumerate(st.session_state.db):
        if search in w['English'].lower() or search in w['Arabic']:
            cols = st.columns([3, 1])
            cols[0].write(f"**{i+1}. {w['English']}** = {w['Arabic']}")
            if cols[1].button("🔊", key=f"voc_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['English']}&type=2")

# --- 7. بقية الغرف (الاختبار والطبيعة) ---
elif st.session_state.page == "game":
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    word = st.session_state.current_word
    st.markdown(f"<div class='royal-card'><h1 class='gold-text'>{word['English']}</h1><p>ما الترجمة الصحيحة؟</p></div>", unsafe_allow_html=True)
    ans = st.text_input("الترجمة:").strip()
    if st.button("تحقق ✅"):
        if ans == word['Arabic']:
            st.session_state.score += 50
            st.session_state.streak += 1
            st.success("أحسنت!")
            st.session_state.current_word = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"خطأ! الترجمة: {word['Arabic']}")
            st.session_state.streak = 0

elif st.session_state.page == "nature":
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.video("https://youtu.be/0wt-HbRw_pw?si=IJ23Q_Mcbb07Kdny")
