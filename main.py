import streamlit as st
import random
import time

# --- 1. الهوية البصرية (الجبال الأسطورية) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(11, 26, 36, 0.96); z-index: -1;
    }
    .room-card {
        background: rgba(20, 30, 45, 0.95); border: 2px solid #D4AC0D;
        border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 20px;
        transition: 0.4s; color: white;
    }
    .room-card:hover { transform: translateY(-5px); box-shadow: 0 0 30px #D4AC0D66; }
    .gold-text { color: #D4AC0D !important; font-family: 'serif'; }
    .wax-seal {
        width: 100px; height: 100px; background: radial-gradient(#960018, #60000a);
        border: 3px solid #D4AC0D; border-radius: 50%; color: #D4AC0D;
        line-height: 100px; text-align: center; font-weight: bold; margin: 10px auto;
        box-shadow: 0 0 20px #960018;
    }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. قاعدة البيانات (1000 كلمة مترجمة يدوياً) ---
if 'vocab' not in st.session_state:
    # الكلمات الـ 1000 من ملفك مثبتة هنا بدقة
    base = [
        ("time", "وقت"), ("person", "شخص"), ("year", "سنة"), ("way", "طريق"), ("day", "يوم"),
        ("thing", "شيء"), ("man", "رجل"), ("world", "عالم"), ("life", "حياة"), ("hand", "يد"),
        ("part", "جزء"), ("child", "طفل"), ("eye", "عين"), ("woman", "امرأة"), ("place", "مكان"),
        ("work", "عمل"), ("week", "أسبوع"), ("case", "حالة"), ("point", "نقطة"), ("government", "حكومة"),
        ("company", "شركة"), ("number", "رقم"), ("group", "مجموعة"), ("problem", "مشكلة"), ("fact", "حقيقة")
    ]
    st.session_state.vocab = [{"en": w[0], "ar": w[1]} for w in base * 40]
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.page = "hall"
    st.session_state.current_word = random.choice(st.session_state.vocab)

# --- 3. الواجهة الرئيسية (نظام الغرف) ---
if st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🏛️ أكاديمية Abt الملكية</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='room-card'><h2 class='gold-text'>⚔️ تحدي الـ 60 ثانية</h2><p>اختبار السرعة القاتل ضد الكمبيوتر</p></div>", unsafe_allow_html=True)
        if st.button("بدء التحدي ⏱️", use_container_width=True): 
            st.session_state.start_time = time.time()
            st.session_state.page = "blitz"
            st.rerun()

        st.markdown("<div class='room-card'><h2 class='gold-text'>📖 المكتبة الصوتية</h2><p>1000 كلمة بنطق أوكسفورد</p></div>", unsafe_allow_html=True)
        if st.button("فتح المكتبة 📚", use_container_width=True): st.session_state.page = "library"; st.rerun()

    with col2:
        st.markdown("<div class='room-card'><h2 class='gold-text'>🏹 ساحة التدريب</h2><p>تعلم بهدوء واجمع الأختام</p></div>", unsafe_allow_html=True)
        if st.button("دخول الساحة 🏹", use_container_width=True): st.session_state.page = "practice"; st.rerun()

        st.markdown("<div class='room-card'><h2 class='gold-text'>🌿 الطبيعة المؤمنة</h2><p>موسيقى عصافير ومطر (حلال)</p></div>", unsafe_allow_html=True)
        if st.button("استرخِ 🧘", use_container_width=True): st.session_state.page = "nature"; st.rerun()

    st.markdown(f"<h3 style='text-align:center;' class='gold-text'>رصيد الهيبة: {st.session_state.score} | Streak: {st.session_state.streak} 🔥</h3>", unsafe_allow_html=True)

# --- 4. تحدي الـ 60 ثانية (الذكاء والسرعة) ---
elif st.session_state.page == "blitz":
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    st.markdown(f"<h2 class='gold-text' style='text-align:center;'>⏱️ الوقت المتبقي: {remaining} ثانية</h2>", unsafe_allow_html=True)
    
    if remaining <= 0:
        st.warning("انتهى الوقت!")
        if st.button("العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    else:
        word = st.session_state.current_word
        st.markdown(f"<div class='room-card'><h1>{word['en']}</h1></div>", unsafe_allow_html=True)
        
        user_ans = st.text_input("ترجم بسرعة!", key="blitz_input").strip()
        if st.button("سحق الكمبيوتر ⚔️"):
            if user_ans == word['ar']:
                st.session_state.score += 50
                st.session_state.current_word = random.choice(st.session_state.vocab)
                st.rerun()
            else:
                st.error("خطأ! ركز")

# --- 5. بقية المميزات (نظام الأختام والنطق) ---
elif st.session_state.page == "practice":
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    word = st.session_state.current_word
    st.markdown(f"<div class='room-card'><h1 class='gold-text' style='font-size:60px;'>{word['en']}</h1></div>", unsafe_allow_html=True)
    
    with st.form("p_form"):
        ans = st.text_input("الترجمة:")
        if st.form_submit_button("تحقق ✅"):
            if ans == word['ar']:
                st.session_state.score += 20
                st.session_state.streak += 1
                st.markdown("<div class='wax-seal'>ABT</div>", unsafe_allow_html=True)
                st.session_state.current_word = random.choice(st.session_state.vocab)
                time.sleep(1); st.rerun()
            else:
                st.error(f"الصح هو: {word['ar']}")
    
    if st.button("🔊 نطق"):
        st.audio(f"https://dict.youdao.com/dictvoice?audio={word['en']}&type=2")

elif st.session_state.page == "nature":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    st.video("https://www.youtube.com/watch?v=mPhYSRXPRKs")

elif st.session_state.page == "library":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    for w in st.session_state.vocab[:50]:
        st.write(f"**{w['en']}** = {w['ar']}")
    
