import streamlit as st
import pandas as pd
import random
import time
import requests
import re

# --- 1. تصميم الواجهة (الخلفية الجبلية الكاملة) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-container {
        background: rgba(0, 0, 0, 0.85);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #D4AC0D;
        color: white;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; text-align: center; }
    .stButton>button {
        background-color: #D4AC0D !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الربط بملف vocab.csv (قراءة 1011 كلمة) ---
@st.cache_data
def load_all_vocab_fix():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    all_words = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                # التحقق من وجود الفاصل ' - ' لضمان جلب الكلمة وترجمتها
                if ' - ' in line:
                    parts = line.split(' - ')
                    # تنظيف الإنجليزي من الأرقام (مثل 1. Time)
                    eng = re.sub(r'^\d+\.\s*', '', parts[0]).strip()
                    ara = parts[1].strip()
                    if eng and ara:
                        all_words.append({"English": eng, "Arabic": ara})
            
            if len(all_words) > 0:
                return all_words
    except:
        pass
    # احتياطي في حال فشل الرابط تماماً
    return [{"English": "Mountain", "Arabic": "جبل"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_all_vocab_fix()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

def speak(word):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")

# --- 4. غرف الأكاديمية (داخل الحاوية) ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # (1) غرفة الدعاء
    if st.session_state.page == "dua":
        st.markdown("<h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='text-align:center; font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>", unsafe_allow_html=True)
        if st.button("آمين - دخول القصر الجبلي"):
            st.session_state.page = "hall"; st.rerun()

    # (2) القصر الرئيسي
    elif st.session_state.page == "hall":
        st.markdown("<h1 class='gold-text'>🏔️ قصر Abt الملكي 🏔️</h1>", unsafe_allow_html=True)
        # هنا سيظهر لك الرقم 1011 بدلاً من 1
        st.markdown(f"<p style='text-align:center;'>تم ربط القاموس: <b>{len(st.session_state.db)}</b> كلمة جاهزة ✅</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 القاموس والنطق (1011 كلمة)"): st.session_state.page = "dict"; st.rerun()
            if st.button("✍️ اختبار التحقق"): st.session_state.page = "test"; st.rerun()
        with col2:
            if st.button("⏳ تحدي 60 ثانية 🔥"): 
                st.session_state.start_time = time.time()
                st.session_state.q_word = random.choice(st.session_state.db)
                st.session_state.page = "blitz"; st.rerun()
            if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()

    # (3) القاموس الشامل (يعرض كل كلماتك)
    elif st.session_state.page == "dict":
        if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
        st.markdown("<h2 class='gold-text'>📖 مكتبة الكلمات الكاملة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في الـ 1011 كلمة:")
        # فلترة ذكية
        filtered = [w for w in st.session_state.db if search.lower() in w['English'].lower() or search in w['Arabic']]
        st.write(f"تم إيجاد {len(filtered)} كلمة")
        for i, w in enumerate(filtered[:100]): # عرض 100 لتجنب البطء
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"v_{i}"): speak(w['English'])

    # (4) تحدي 60 ثانية (مع زر التحقق الملكي)
    elif st.session_state.page == "blitz":
        if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
        rem = 60 - int(time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
        else:
            st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
            word = st.session_state.q_word
            st.markdown(f"<h2 style='text-align:center;'>ترجم: <span class='gold-text'>{word['English']}</span></h2>", unsafe_allow_html=True)
            if st.button("اسمع 🔊"): speak(word['English'])
            ans = st.text_input("الإجابة:")
            if st.button("تحقق من الكلمة ✅"):
                if ans.strip() == word['Arabic']:
                    st.session_state.score += 50
                    st.session_state.q_word = random.choice(st.session_state.db)
                    st.success("صح!"); time.sleep(0.5); st.rerun()
                else:
                    st.warning("حاول مرة أخرى!")

    st.markdown('</div>', unsafe_allow_html=True)
    
