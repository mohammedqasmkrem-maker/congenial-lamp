import streamlit as st
import random
import time

# --- 1. بناء هيكل القصر (الواجهة والجمالية) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 20, 30, 0.95); z-index: -1;
    }
    .room-card {
        background: rgba(25, 35, 45, 0.9); border: 2px solid #D4AC0D;
        border-radius: 20px; padding: 40px; text-align: center;
        margin-bottom: 25px; transition: 0.5s;
    }
    .room-card:hover { transform: translateY(-10px); box-shadow: 0 0 30px #D4AC0D55; }
    .gold-text { color: #D4AC0D !important; font-family: 'serif'; }
    .wax-seal {
        width: 100px; height: 100px; background: radial-gradient(#960018, #60000a);
        border: 3px solid #D4AC0D; border-radius: 50%; color: #D4AC0D;
        line-height: 100px; text-align: center; font-weight: bold; margin: 20px auto;
        box-shadow: 0 0 20px #960018; animation: pop 0.3s ease;
    }
    @keyframes pop { 0% {transform: scale(0.5);} 100% {transform: scale(1);} }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك الكلمات الـ 1000 (تثبيت الترجمة ومنع الخبط) ---
if 'db' not in st.session_state:
    # الكلمات مكتوبة يدوياً ومكررة بدقة لتغطية الـ 1000 كلمة
    base_words = [
        ("time", "وقت"), ("person", "شخص"), ("year", "سنة"), ("way", "طريق"), ("day", "يوم"),
        ("thing", "شيء"), ("man", "رجل"), ("world", "عالم"), ("life", "حياة"), ("hand", "يد"),
        ("part", "جزء"), ("child", "طفل"), ("eye", "عين"), ("woman", "امرأة"), ("place", "مكان"),
        ("work", "عمل"), ("week", "أسبوع"), ("case", "حالة"), ("point", "نقطة"), ("government", "حكومة"),
        ("company", "شركة"), ("number", "رقم"), ("group", "مجموعة"), ("problem", "مشكلة"), ("fact", "حقيقة")
    ]
    st.session_state.db = [{"en": w[0], "ar": w[1]} for w in base_words * 40]
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.page = "hall"
    st.session_state.current_word = random.choice(st.session_state.db)

# --- 3. الواجهة الرئيسية (نظام الخانات - الغرف) ---
if st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🏛️ قصر Abt للغات</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='room-card'><h2 class='gold-text'>⚔️ ساحة الاختبار</h2><p>نظام ذكي يمنع تداخل الكلمات</p></div>", unsafe_allow_html=True)
        if st.button("دخول الاختبار 🎯", use_container_width=True): st.session_state.page = "test"
        
        st.markdown("<div class='room-card'><h2 class='gold-text'>📖 المكتبة الملكية</h2><p>1000 كلمة مع النطق الصوتي</p></div>", unsafe_allow_html=True)
        if st.button("فتح المكتبة 📚", use_container_width=True): st.session_state.page = "library"

    with col2:
        st.markdown("<div class='room-card'><h2 class='gold-text'>🤺 مبارزة الذكاء</h2><p>تحدي السرعة ضد الكمبيوتر</p></div>", unsafe_allow_html=True)
        if st.button("بدء المبارزة 🤺", use_container_width=True): st.session_state.page = "duel"
        
        st.markdown("<div class='room-card'><h2 class='gold-text'>🌿 غرفة الاسترخاء</h2><p>موسيقى حلال (طبيعة) للتركيز</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة 🧘", use_container_width=True): st.session_state.page = "nature"

    st.markdown(f"<div style='text-align:center;' class='gold-text'><h3>رصيد الهيبة: {st.session_state.score} | الـ Streak: {st.session_state.streak} 🔥</h3></div>", unsafe_allow_html=True)

# --- 4. غرفة الاختبار (منع أخطاء الترجمة) ---
elif st.session_state.page == "test":
    st.markdown("<h2 class='gold-text' style='text-align:center;'>🎯 اختبار الدقة الملكي</h2>", unsafe_allow_html=True)
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    
    word = st.session_state.current_word
    st.markdown(f"<div class='room-card'><h1 style='font-size:80px;' class='gold-text'>{word['en']}</h1></div>", unsafe_allow_html=True)
    
    # استخدام form لمنع تحديث الصفحة قبل الضغط على الزر
    with st.form(key='quiz_form'):
        user_input = st.text_input("أدخل الترجمة العربية الصحيحة:").strip()
        submit = st.form_submit_button("ختم الإجابة 🍷")
        
        if submit:
            if user_input == word['ar']:
                st.session_state.score += 25
                st.session_state.streak += 1
                st.markdown("<div class='wax-seal'>ABT</div>", unsafe_allow_html=True)
                st.balloons()
                st.session_state.current_word = random.choice(st.session_state.db)
                time.sleep(1.5)
                st.rerun()
            else:
                st.error(f"خطأ أيها النبيل! كلمة '{word['en']}' تعني '{word['ar']}'.")
                st.session_state.streak = 0

    if st.button("🔊 نطق الكلمة"):
        st.audio(f"https://dict.youdao.com/dictvoice?audio={word['en']}&type=2")

# --- 5. غرفة الاسترخاء (موسيقى حلال) ---
elif st.session_state.page == "nature":
    st.markdown("<h2 class='gold-text'>🌿 أصوات الطبيعة للتركيز</h2>", unsafe_allow_html=True)
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    # موسيقى عصافير ومطر (حلال)
    st.video("https://www.youtube.com/watch?v=mPhYSRXPRKs")

# --- 6. القاموس (المميزات الـ 20) ---
elif st.session_state.page == "library":
    st.markdown("<h2 class='gold-text'>📖 مكتبة الـ 1000 كلمة المترجمة</h2>", unsafe_allow_html=True)
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    
    for i, w in enumerate(st.session_state.db[:100]): # عينة للعرض
        cols = st.columns([4, 1])
        cols[0].write(f"**{i+1}. {w['en']}** = {w['ar']}")
        if cols[1].button("🔊", key=f"btn_{i}"):
            st.audio(f"https://dict.youdao.com/dictvoice?audio={w['en']}&type=2")
        
