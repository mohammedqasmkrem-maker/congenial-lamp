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

# --- 2. محرك الجمل والبيانات (ربط ملف vocab.csv) ---
@st.cache_data
def load_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        # مصفوفة جمل افتراضية مرتبطة بالكلمات الشائعة في ملفك
        sentences = {
            "Time": "I don't have enough __.", "Person": "He is a good __.",
            "Year": "Happy new __!", "Way": "Show me the __.",
            "Day": "Have a nice __.", "World": "The __ is small."
        }
        data = []
        for _, row in df.iterrows():
            en = row['English'].strip()
            data.append({
                "en": en, 
                "ar": row['Arabic'], 
                "sentence": sentences.get(en, f"How do you spell '{en}'?") 
            })
        return data
    except:
        return [{"en": "Time", "ar": "الوقت", "sentence": "I don't have enough __."}]

# --- 3. تهيئة النظام (حل AttributeError) ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'page' not in st.session_state: st.session_state.page = "hall"
if 'db' not in st.session_state: st.session_state.db = load_vocab()
if 'current_word' not in st.session_state: st.session_state.current_word = random.choice(st.session_state.db)

# --- 4. الواجهة الرئيسية ---
if st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='royal-card'><h2 class='gold-text'>👤 الملف الشخصي</h2><p>النقاط: {st.session_state.score} | الـ Streak: {st.session_state.streak}</p></div>", unsafe_allow_html=True)
        if st.button("فتح القاموس 📖", use_container_width=True): st.session_state.page = "dict"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>✍️ تحدي الـ 60 نقطة</h2><p>أكمل الفراغ في الجملة</p></div>", unsafe_allow_html=True)
        if st.button("بدء التحدي ⚔️", use_container_width=True): st.session_state.page = "game"

    st.markdown(f"<p style='text-align:center;'><a href='https://share.streamlit.io/user/mqasmkrem-a11y' style='color:#D4AC0D;'>رابط المنصة الرسمية</a></p>", unsafe_allow_html=True)

# --- 5. منطق تحدي الجمل (60 نقطة) ---
elif st.session_state.page == "game":
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    word = st.session_state.current_word
    
    st.markdown(f"<div class='royal-card'><h2 class='gold-text'>{word['sentence']}</h2><p>(الترجمة: {word['ar']})</p></div>", unsafe_allow_html=True)
    
    ans = st.text_input("اكتب الكلمة الناقصة بالإنجليزية:").strip().lower()
    if st.button("تحقق ✅"):
        if ans == word['en'].lower():
            st.session_state.score += 60  # تم ضبط الاختبار على 60 نقطة
            st.session_state.streak += 1
            st.success("إجابة ملكية! +60 نقطة")
            st.session_state.current_word = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"خطأ! الكلمة الصحيحة هي: {word['en']}")
            st.session_state.streak = 0

# --- 6. القاموس الملكي مع البحث ---
elif st.session_state.page == "dict":
    st.markdown("<h2 class='gold-text' style='text-align:center;'>📖 المكتبة الشاملة</h2>", unsafe_allow_html=True)
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    
    search = st.text_input("🔍 ابحث عن كلمة:").lower()
    for i, w in enumerate(st.session_state.db):
        if search in w['en'].lower() or search in w['ar']:
            cols = st.columns([3, 1])
            cols[0].write(f"**{w['en']}** = {w['ar']}")
            if cols[1].button("🔊", key=f"s_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['en']}&type=2")
            
