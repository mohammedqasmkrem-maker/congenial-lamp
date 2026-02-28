import streamlit as st
import random

# --- 1. إعدادات الصفحة (تصميم بسيط ومرتب) ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", page_icon="💡")

# تنسيق الألوان (عربي أخضر، إنجليزي أزرق)
st.markdown("""
    <style>
    .ar-style { color: #2ecc71; font-size: 25px; font-weight: bold; }
    .en-style { color: #3498db; font-size: 25px; font-weight: bold; }
    .stButton>button { width: 100%; height: 3em; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. القاموس (الجزء الأول) ---
if 'dictionary' not in st.session_state:
    st.session_state.dictionary = [
        {"en": "Success", "ar": "نجاح", "hint": "عكس الفشل"},
        {"en": "Knowledge", "ar": "معرفة", "hint": "تأتي من الدراسة"},
        {"en": "Light", "ar": "ضوء", "hint": "يخرج من المصباح"},
        {"en": "Friend", "ar": "صديق", "hint": "شخص تحبه"},
        {"en": "Future", "ar": "مستقبل", "hint": "الأيام الجاية"}
    ]

# --- 3. حفظ النقاط (عشان ما تصفر) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.dictionary)

# --- 4. واجهة الاختبار ---
st.title("💡 اختبار مصباح لطيف")
st.write(f"### مجموع نقاطك الحالي: {st.session_state.score} 🏆")

st.markdown("---")
st.write("ما معنى الكلمة التالية؟")
st.markdown(f"<div class='en-style'>{st.session_state.current_word['en']}</div>", unsafe_allow_html=True)

# إدخال الجواب
user_ans = st.text_input("اكتب الإجابة بالعربي هنا:", key="ans_input").strip()

col1, col2 = st.columns(2)

with col1:
    if st.button("تحقق ✅"):
        if user_ans == st.session_state.current_word['ar']:
            st.success("صح! +10 نقاط")
            st.session_state.score += 10
            # تغيير الكلمة بعد الصح
            st.session_state.current_word = random.choice(st.session_state.dictionary)
            st.rerun()
        else:
            st.error(f"خطأ! الإجابة كانت: {st.session_state.current_word['ar']}")
            # ميزة التغيير الفوري عند الخطأ كما طلبت
            st.session_state.current_word = random.choice(st.session_state.dictionary)
            st.info("تم الانتقال لكلمة جديدة.. حاول مرة ثانية")
            st.rerun()

with col2:
    if st.button("💡 مساعدة"):
        st.warning(f"تلميح: {st.session_state.current_word['hint']}")

# --- 5. القاموس (مرتب بالألوان) ---
st.markdown("---")
with st.expander("📖 القاموس"):
    for item in st.session_state.dictionary:
        st.markdown(f"<span class='en-style'>{item['en']}</span> = <span class='ar-style'>{item['ar']}</span>", unsafe_allow_html=True)

# --- 6. الرابط المطلوب في الأخير ---
st.markdown("---")
st.markdown(f"[🔗 رابط إدارة التطبيق](https://share.streamlit.io/user/mqasmkrem-a11y)")
