import streamlit as st
import pandas as pd
import random
import os

# 1. إعداد الصفحة (لتفتح بشكل كامل ومباشر)
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide", page_icon="🎮")

# 2. دالة تحميل البيانات (تعمل في الخلفية فوراً)
@st.cache_data
def load_data():
    file_name = 'vocab.csv'
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name, header=None, names=['full_line'], sep='|', engine='python')
            df['level'] = 'سهل'
            if len(df) > 300: df.loc[300:700, 'level'] = 'متوسط'
            if len(df) > 700: df.loc[700:, 'level'] = 'صعب'
            return df
        except: return None
    return None

df = load_data()

# 3. واجهة التطبيق المباشرة
if df is not None:
    # القائمة الجانبية للتنقل السريع
    menu = st.sidebar.radio("اختر القسم:", ["📖 البحث الفوري", "🎯 ابدأ اللعبة الآن"])

    if menu == "📖 البحث الفوري":
        st.title("🔍 ابحث عن أي كلمة")
        search = st.text_input("اكتب الكلمة هنا تظهر لك النتيجة فوراً:", placeholder="مثلاً: Apple")
        
        if search:
            results = df[df['full_line'].str.contains(search, case=False)]
            st.table(results[['level', 'full_line']])
        else:
            st.write("جميع الكلمات المتاحة:")
            st.dataframe(df[['level', 'full_line']], use_container_width=True)

    elif menu == "🎯 ابدأ اللعبة الآن":
        st.title("🎯 تحدي الـ 1000 كلمة")
        lvl = st.selectbox("اختر الصعوبة:", ["سهل", "متوسط", "صعب"])
        level_df = df[df['level'] == lvl]

        if st.button("كلمة جديدة 🔄") or 'word' not in st.session_state:
            st.session_state.word = random.choice(level_df['full_line'].values)
            st.session_state.show = False

        full_word = st.session_state.word
        eng = full_word.split('-')[0].strip() if '-' in full_word else full_word
        arb = full_word.split('-')[1].strip() if '-' in full_word else "ترجم"

        st.info(f"### كيف تترجم هذه الكلمة؟ \n # {eng}")
        
        if st.button("إظهار الحل 👀"):
            st.session_state.show = True
        
        if st.session_state.show:
            st.success(f"### المعنى هو: {arb}")

else:
    st.error("⚠️ ملف vocab.csv غير موجود بجانب الكود في GitHub.")
            
