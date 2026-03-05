import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.97); z-index: -1; }
    .royal-card { background: rgba(20, 35, 30, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .timer-text { font-size: 30px; color: #ff4b4b; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك تكوين الجمل الذكي (Automated Sentence Builder) ---
@st.cache_data
def load_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        
        # قوالب ذكية لتكوين الجمل تلقائياً لكل الكلمات
        templates = [
            "I like to use my __.", "Can you show me the __?", 
            "This is a very important __.", "Where is the __?",
            "I will check the __ tomorrow.", "It was a great __."
        ]
        
        data = []
        for _, row in df.iterrows():
            en_word = row['English'].strip()
            data.append({
                "en": en_word, 
                "ar": row['Arabic'], 
                "sentence": random.choice(templates).replace("__", f"[{en_word}]").replace(f"[{en_word}]", "__")
            })
        return data
    except:
        return [{"en": "Time", "ar": "الوقت", "sentence": "I need more __."}]

# --- 3. تهيئة الحالة (Session State) ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "hall"
if 'db' not in st.session_state: st.session_state.db = load_vocab()
if 'start_time' not in st.session_state: st.session_state.start_time = None

# --- 4. الواجهة الرئيسية ---
if st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='royal-card'><h2 class='gold-text'>👤 ملفك</h2><p>النقاط: {st.session_state.score}</p></div>", unsafe_allow_html=True)
        if st.button("فتح القاموس 📖", use_container_width=True): st.session_state.page = "dict"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>⏳ تحدي الـ 60 ثانية</h2><p>ذكاء اصطناعي ضد السرعة</p></div>", unsafe_allow_html=True)
        if st.button("ابدأ التحدي السريع ⚔️", use_container_width=True): 
            st.session_state.page = "blitz"
            st.session_state.start_time = time.time()
            st.session_state.current_word = random.choice(st.session_state.db)
            st.rerun()

# --- 5. تحدي الـ 60 ثانية وتكوين الجمل ---
elif st.session_state.page == "blitz":
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    if remaining <= 0:
        st.error("💥 انتهى الوقت!")
        st.markdown(f"<div class='royal-card'><h2>مجموع نقاطك: {st.session_state.score}</h2></div>", unsafe_allow_html=True)
        if st.button("العودة للقصر"): 
            st.session_state.page = "hall"
            st.rerun()
    else:
        st.markdown(f"<p class='timer-text'>⏳ الوقت المتبقي: {remaining} ثانية</p>", unsafe_allow_html=True)
        word = st.session_state.current_word
        
        st.markdown(f"<div class='royal-card'><h2 class='gold-text'>{word['sentence']}</h2><p>ترجمة الكلمة الناقصة: {word['ar']}</p></div>", unsafe_allow_html=True)
        
        user_input = st.text_input("اكتب الكلمة الناقصة بالإنجليزية:", key="input_box").strip().lower()
        
        if st.button("إرسال ✅"):
            if user_input == word['en'].lower():
                st.session_state.score += 60
                st.session_state.current_word = random.choice(st.session_state.db)
                st.success("صح! +60 نقطة")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(f"خطأ! الكلمة هي: {word['en']}")

# --- 6. القاموس الملكي ---
elif st.session_state.page == "dict":
    st.markdown("<h2 class='gold-text' style='text-align:center;'>📖 القاموس الشامل</h2>", unsafe_allow_html=True)
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    
    search = st.text_input("🔍 ابحث في الـ 1011 كلمة:").lower()
    for i, w in enumerate(st.session_state.db):
        if search in w['en'].lower() or search in w['ar']:
            st.write(f"**{w['en']}** : {w['ar']}")
            
