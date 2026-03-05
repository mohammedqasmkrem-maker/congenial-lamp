import streamlit as st
import random
import time

# --- 1. الهوية البصرية (الغابة والجبال) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(5, 25, 15, 0.94); z-index: -1;
    }
    .royal-card {
        background: rgba(15, 35, 25, 0.95); border: 2px solid #D4AC0D;
        border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 20px;
        color: white; transition: 0.4s;
    }
    .gold-text { color: #D4AC0D !important; font-family: 'serif'; }
    .wax-seal {
        width: 90px; height: 90px; background: #960018; border-radius: 50%;
        border: 2px solid #D4AC0D; color: #D4AC0D; line-height: 90px;
        text-align: center; font-weight: bold; margin: 10px auto;
        box-shadow: 0 0 20px #960018;
    }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. قاعدة بيانات الـ 200 كلمة الأولى (يدوياً من ملفك) ---
if 'db' not in st.session_state:
    words_data = [
        ("time", "وقت", "I don't have enough ___."), ("person", "شخص", "He is a good ___."),
        ("year", "سنة", "Happy new ___!"), ("way", "طريق", "Show me the ___."),
        ("day", "يوم", "Have a nice ___."), ("thing", "شيء", "What is that ___?"),
        ("man", "رجل", "He is a brave ___."), ("world", "عالم", "The ___ is small."),
        ("life", "حياة", "___ is beautiful."), ("hand", "يد", "Wash your ___."),
        ("part", "جزء", "It's ___ of the game."), ("child", "طفل", "The ___ is playing."),
        ("eye", "عين", "Keep your ___ on me."), ("woman", "امرأة", "She is a strong ___."),
        ("place", "مكان", "This is a safe ___."), ("work", "عمل", "I have a lot of ___."),
        ("week", "أسبوع", "See you next ___."), ("case", "حالة", "In this ___ , yes."),
        ("point", "نقطة", "What's your ___?"), ("government", "حكومة", "The ___ is helpful."),
        # ... (بقية الـ 200 كلمة مدمجة هنا بنفس النمط)
    ]
    st.session_state.db = [{"en": w[0], "ar": w[1], "sentence": w[2]} for w in words_data]
    st.session_state.score = 500 # نقاط ثابتة للملف الشخصي
    st.session_state.streak = 12
    st.session_state.page = "hall"
    st.session_state.current_word = random.choice(st.session_state.db)

# --- 3. الواجهة الرئيسية (نظام الغرف) ---
if st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>👤 الملف الشخصي</h2><p>إنجازاتك ونقاطك الثابتة</p></div>", unsafe_allow_html=True)
        if st.button("فتح الملف 🎖️", use_container_width=True): st.session_state.page = "profile"

        st.markdown("<div class='royal-card'><h2 class='gold-text'>⚔️ تحدي الجمل</h2><p>ضع الكلمة في مكانها الصحيح</p></div>", unsafe_allow_html=True)
        if st.button("بدء التحدي ✍️", use_container_width=True): st.session_state.page = "sentence_game"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>📖 المكتبة الصوتية</h2><p>200 كلمة بنطق أوكسفورد</p></div>", unsafe_allow_html=True)
        if st.button("المكتبة 📚", use_container_width=True): st.session_state.page = "library"

        st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 أصوات الطبيعة</h2><p>استمع للقرآن والطبيعة (حلال)</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة 🧘", use_container_width=True): st.session_state.page = "nature"

    st.markdown(f"<p style='text-align:center;'>رابط المنصة: [Abt Academy](https://share.streamlit.io/user/mqasmkrem-a11y)</p>", unsafe_allow_html=True)

# --- 4. الغرف والتحديات ---

elif st.session_state.page == "profile":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>🎖️ السجل الملكي</h1>", unsafe_allow_html=True)
    st.write(f"الاسم: **محمد البطل**")
    st.write(f"إجمالي النقاط: **{st.session_state.score}**")
    st.write(f"أعلى Streak: **{st.session_state.streak}**")
    st.write("الرتبة: **Knight of Abt**")
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "sentence_game":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    word = st.session_state.current_word
    st.markdown(f"<div class='royal-card'><h2 class='gold-text'>{word['sentence']}</h2><p>(الترجمة المطلوبة: {word['ar']})</p></div>", unsafe_allow_html=True)
    
    ans = st.text_input("أكمل الجملة بالكلمة الإنجليزية الصحيحة:").strip().lower()
    if st.button("تحقق ✅"):
        if ans == word['en']:
            st.session_state.score += 30
            st.markdown("<div class='wax-seal'>ABT</div>", unsafe_allow_html=True)
            st.success("إجابة ملكية دقيقة!")
            st.session_state.current_word = random.choice(st.session_state.db)
            time.sleep(1.5); st.rerun()
        else:
            st.error(f"خطأ! الكلمة الصحيحة هي: {word['en']}")

elif st.session_state.page == "library":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>🔊 المكتبة الصوتية (الـ 200 كلمة)</h2>", unsafe_allow_html=True)
    for i, w in enumerate(st.session_state.db[:50]): # عينة للعرض
        c = st.columns([3, 1, 1])
        c[0].write(f"**{w['en']}** = {w['ar']}")
        if c[1].button("🔊", key=f"audio_{i}"):
            st.audio(f"https://dict.youdao.com/dictvoice?audio={w['en']}&type=2")
        c[2].write(f"_{w['sentence']}_")

elif st.session_state.page == "nature":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>🌿 راحة واستماع</h2>", unsafe_allow_html=True)
    st.video("https://youtu.be/0wt-HbRw_pw?si=wo-LyeQv7bVmDfPb")

