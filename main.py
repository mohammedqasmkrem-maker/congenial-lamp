import streamlit as st
import random
import sqlite3

# --- 1. إعدادات الصفحة والوضع الليلي ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .en-style { color: #3498db; font-size: 35px; font-weight: bold; text-align: center; }
    .ar-style { color: #2ecc71; font-size: 25px; font-weight: bold; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3440,#2e3440); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والقاموس (١٠٠ جزء) ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'words' not in st.session_state:
    st.session_state.words = [
        {"en": "Tell", "ar": "يخبر", "hint": "يعطي معلومة لشخص"},
        {"en": "Not", "ar": "ليس", "hint": "للنفي"},
        {"en": "He", "ar": "هو", "hint": "للمذكر"},
        {"en": "As", "ar": "كما", "hint": "للتشبيه"},
        {"en": "You", "ar": "أنت", "hint": "للمخاطب"}
    ]
if 'current' not in st.session_state: st.session_state.current = random.choice(st.session_state.words)

# --- 3. القائمة الجانبية (القاموس ونظام المستويات) ---
with st.sidebar:
    st.title("📖 القاموس والخيارات")
    st.markdown("---")
    choice = st.radio("اختر القسم:", ["🎯 الاختبار", "📖 القاموس الكامل", "📊 لوحة الصدارة"])
    
    st.markdown("---")
    level = st.selectbox("المستوى:", ["Easy", "Medium", "Hard"])
    
    if st.button("🔄 تصفير النقاط (Reset)"):
        st.session_state.score = 0
        st.rerun()

# --- 4. الواجهة الرئيسية (الاختبار) ---
if choice == "🎯 الاختبار":
    st.title("💡 اختبار مصباح لطيف")
    st.subheader(f"🏆 نقاطك الثابتة: {st.session_state.score}")
    
    # مربع الاختبار (مثل الصورة التي أرسلتها)
    st.markdown(f"<div style='border: 2px solid #f1c40f; padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)
    st.markdown(f"<div class='en-style'>{st.session_state.current['en']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    ans = st.text_input("👇 اكتب الحل بالعربي هنا", key="quiz_input").strip()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("تحقق ✅"):
            if ans == st.session_state.current['ar']:
                st.success("✨ أحسنت! كبل للكلمة التالية")
                st.session_state.score += 10
                st.session_state.current = random.choice(st.session_state.words)
                st.rerun()
            else:
                st.error("❌ خطأ! تبقى نفس الكلمة للحفظ")
    with col2:
        if st.button("🔊 نطق (مرتين)"):
            for _ in range(2):
                st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.current['en']}&tl=en&client=tw-ob")
    with col3:
        if st.button("💡 مساعدة"):
            st.info(f"تلميح: {st.session_state.current['hint']}")

# --- 5. صفحة القاموس (بجانب الاختبار في القائمة) ---
elif choice == "📖 القاموس الكامل":
    st.title("📖 القاموس المرتب")
    for i, item in enumerate(st.session_state.words, 1):
        col_en, col_ar, col_sound = st.columns([1, 1, 1])
        with col_en: st.markdown(f"<div class='en-style' style='font-size:20px;'>{i}. {item['en']}</div>", unsafe_allow_html=True)
        with col_ar: st.markdown(f"<div class='ar-style'>{item['ar']}</div>", unsafe_allow_html=True)
        with col_sound:
             if st.button(f"🔊", key=f"btn_{i}"):
                 st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={item['en']}&tl=en&client=tw-ob")

# --- 6. الرابط المطلوب في الأسفل ---
st.markdown("---")
st.markdown(f"[🔗 رابط إدارة تطبيقك](https://share.streamlit.io/user/mqasmkrem-a11y)")
    
