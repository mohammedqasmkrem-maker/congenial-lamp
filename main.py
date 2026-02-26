import streamlit as st
import pandas as pd
import random

# إعداد واجهة الأكاديمية
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="centered")

@st.cache_data
def load_data():
    # قراءة ملفك كما هو موضح في الصورة
    return pd.read_csv('vocab.csv', header=None, names=['text'])

try:
    df = load_data()
    st.sidebar.title("💎 خيارات التعلم")
    mode = st.sidebar.radio("اختر النمط:", ["🚀 اختبار سريع", "📚 مراجعة شاملة"])

    if mode == "🚀 اختبار سريع":
        st.title("🎯 تحدي الكلمات")
        if 'word' not in st.session_state:
            st.session_state.word = random.choice(df['text'].values)
            st.session_state.reveal = False

        # عرض رقم الكلمة فقط
        num = st.session_state.word.split('.')[0]
        st.markdown(f"<div style='text-align:center; padding:30px; border:2px solid #FF4B4B; border-radius:15px;'><h2>ما هي الكلمة رقم</h2><h1 style='color:#FF4B4B; font-size:60px;'>{num}</h1></div>", unsafe_content=True)

        if st.button("إظهار الكلمة والحل 👀", use_container_width=True):
            st.session_state.reveal = True

        if st.session_state.reveal:
            st.success(f"### الكلمة هي: {st.session_state.word}")
            if st.button("الكلمة التالية ➡️"):
                st.session_state.word = random.choice(df['text'].values)
                st.session_state.reveal = False
                st.rerun()

    else:
        st.title("📖 القاموس التعليمي")
        search = st.text_input("🔍 ابحث عن كلمة:")
        display_df = df[df['text'].str.contains(search, case=False)] if search else df
        for line in display_df.head(50)['text']:
            st.write(f"✅ {line}")

except Exception as e:
    st.error(f"خطأ في الملف: {e}")
    
