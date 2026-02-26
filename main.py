import streamlit as st
import pandas as pd
import random

# إعداد واجهة التطبيق
st.set_page_config(page_title="Word Quiz", layout="centered")

@st.cache_data
def load_data():
    # قراءة الملف الذي يحتوي على الكلمات
    return pd.read_csv('vocab.csv', header=None, names=['full_text'])

try:
    df = load_data()
    st.title("🎯 اختبار الـ 1000 كلمة")
    st.divider()

    # تهيئة الكلمة الحالية في ذاكرة المتصفح
    if 'current_word' not in st.session_state:
        st.session_state.current_word = random.choice(df['full_text'].values)
        st.session_state.show_reveal = False

    st.subheader("ما هو معنى هذه الكلمة؟")
    # عرض رقم الكلمة أو جزء منها للتشويق
    st.info(f"### {st.session_state.current_word.split('.')[0]}. ???")

    if st.button("إظهار الإجابة 👀"):
        st.session_state.show_reveal = True

    if st.session_state.show_reveal:
        st.success(f"### {st.session_state.current_word}")
        
        if st.button("الكلمة التالية ➡️"):
            st.session_state.current_word = random.choice(df['full_text'].values)
            st.session_state.show_reveal = False
            st.rerun()

    st.divider()
    if st.button("كلمة عشوائية أخرى 🎲"):
        st.session_state.current_word = random.choice(df['full_text'].values)
        st.session_state.show_reveal = False
        st.rerun()

except Exception as e:
    st.error("تأكد من وجود ملف vocab.csv في حسابك على GitHub")
    
