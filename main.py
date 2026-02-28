import streamlit as st
import random

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", page_icon="💡", layout="centered")

# تنسيق الألوان (العربية أخضر، الإنجليزية أزرق)
st.markdown("""
    <style>
    .ar-text { color: #2ecc71; font-size: 28px; font-weight: bold; text-align: center; }
    .en-text { color: #3498db; font-size: 28px; font-weight: bold; text-align: center; }
    .score-text { color: #f39c12; font-size: 20px; font-weight: bold; }
    div.stButton > button:first-child { width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. القاموس المرتب (عينة من الكلمات) ---
# يمكنك إضافة المزيد من الكلمات هنا بنفس الترتيب
if 'dictionary' not in st.session_state:
    st.session_state.dictionary = [
        {"en": "Success", "ar": "نجاح", "hint": "عكس الفشل"},
        {"en": "Knowledge", "ar": "معرفة", "hint": "ما نحصل عليه من القراءة"},
        {"en": "Light", "ar": "ضوء", "hint": "يأتي من الشمس أو المصباح"},
        {"en": "Friend", "ar": "صديق", "hint": "شخص نحبه ونثق به"},
        {"en": "Future", "ar": "مستقبل", "hint": "الأيام القادمة"}
    ]

# --- 3. نظام النقاط الثابت (Session State) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_item' not in st.session_state:
    st.session_state.current_item = random.choice(st.session_state.dictionary)

# --- 4. واجهة التطبيق ---
st.title("💡 قاموس واختبار مصباح لطيف")
st.markdown(f"<div class='score-text'>🏆 نقاطك الحالية: {st.session_state.score}</div>", unsafe_allow_html=True)

st.divider()

# عرض الكلمة المراد اختبارها
st.markdown("### ما معنى هذه الكلمة؟")
st.markdown(f"<div class='en-text'>{st.session_state.current_item['en']}</div>", unsafe_allow_html=True)

# إدخال الإجابة
user_input = st.text_input("اكتب المعنى بالعربي:", key="user_ans").strip()

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ تحقق"):
        if user_input == st.session_state.current_item['ar']:
            st.success("إجابة صحيحة! +10 نقاط")
            st.session_state.score += 10
            st.session_state.current_item = random.choice(st.session_state.dictionary)
            st.rerun()
        else:
            st.error(f"خطأ! الإجابة كانت: {st.session_state.current_item['ar']}")
            # تغيير الكلمة فوراً عند الخطأ كما طلبت
            st.session_state.current_item = random.choice(st.session_state.dictionary)
            st.info("جرب حظك مع كلمة جديدة!")
            st.rerun()

with col2:
    if st.button("💡 مساعدة"):
        st.warning(f"تلميح: {st.session_state.current_item['hint']}")

# --- 5. قسم القاموس المرتب ---
st.divider()
with st.expander("📖 عرض القاموس الكامل"):
    for item in st.session_state.dictionary:
        st.markdown(f"🔹 <span class='en-text'>{item['en']}</span> = <span class='ar-text'>{item['ar']}</span>", unsafe_allow_html=True)

# --- 6. الصوت والروابط ---
st.markdown("---")
st.write("🎵 صوت الطبيعة (شلالات):")
# رابط صوت شلالات طبيعي
st.audio("https://www.soundjay.com/nature/sounds/waterfall-01.mp3")

st.markdown("---")
st.markdown(f"[🔗 رابط إدارة التطبيق](https://share.streamlit.io/user/mqasmkrem-a11y)")
