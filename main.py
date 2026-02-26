import streamlit as st
import pandas as pd
import random

# إعداد الصفحة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="centered")

@st.cache_data
def load_data():
    try:
        # قراءة ملفك الجاهز
        df = pd.read_csv('vocab.csv', header=None, names=['text'])
        return df
    except:
        return None

df = load_data()

if df is not None:
    st.sidebar.title("💎 الخيارات")
    mode = st.sidebar.radio("اختر النمط:", ["🎯 اختبار ذكي", "📖 قاموس الكلمات"])

    if mode == "🎯 اختبار ذكي":
        st.title("🎯 تحدي الـ 1000 كلمة")
        
        if 'current_word' not in st.session_state:
            st.session_state.current_word = random.choice(df['text'].values)
            st.session_state.reveal = False

        # عرض رقم الكلمة للتشويق
        word_data = st.session_state.current_word
        st.subheader("هل تعرف معنى هذه الكلمة؟")
        st.info(f"### {word_data.split('.')[0]}") # يعرض الرقم فقط

        if st.button("إظهار الكلمة والترجمة 👀"):
            st.session_state.reveal = True

        if st.session_state.reveal:
            st.success(f"✅ {word_data}")
            if st.button("الكلمة التالية ➡️"):
                st.session_state.current_word = random.choice(df['text'].values)
                st.session_state.reveal = False
                st.rerun()
    else:
        st.title("📖 القاموس الشامل")
        search = st.text_input("🔍 ابحث عن كلمة أو رقم:")
        filtered_df = df[df['text'].str.contains(search, case=False)] if search else df
        for line in filtered_df.head(100)['text']:
            st.write(line)
else:
    st.error("تأكد من وجود ملف vocab.csv في GitHub")
    
