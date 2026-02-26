import streamlit as st
import pandas as pd
import random

# إعداد واجهة احترافية
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide")

# دالة لقراءة السطر كاملاً بدون تقسيم عند الأرقام
@st.cache_data
def load_data():
    try:
        # نقرأ السطر ككتلة واحدة لتجنب ظهور الأرقام فقط
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
        return df
    except:
        return None

df = load_data()

# القائمة الجانبية (هنا تجد القاموس)
st.sidebar.title("📖 الأقسام")
menu = st.sidebar.radio("اختر القسم:", ["🎯 اختبار التحدي", "🔍 القاموس الكامل"])

if df is not None:
    if menu == "🎯 اختبار التحدي":
        st.title("🎯 تحدي الـ 1000 كلمة")
        
        if 'current_word' not in st.session_state:
            st.session_state.current_word = random.choice(df['full_line'].values)
            st.session_state.revealed = False

        # عرض الكلمة بشكل واضح (نخفي الترجمة أولاً)
        raw_word = st.session_state.current_word
        english_only = raw_word.split('-')[0] if '-' in raw_word else raw_word
        
        st.info(f"### خمن معنى: \n # {english_only}")

        if st.button("👀 إظهار الحل والترجمة"):
            st.session_state.revealed = True
        
        if st.session_state.revealed:
            st.success(f"### {st.session_state.current_word}")
            if st.button("➡️ الكلمة التالية"):
                st.session_state.current_word = random.choice(df['full_line'].values)
                st.session_state.revealed = False
                st.rerun()

    elif menu == "🔍 القاموس الكامل":
        st.title("📖 القاموس التفاعلي")
        search = st.text_input("🔍 ابحث عن أي كلمة بالعربي أو الإنجليزي:")
        
        if search:
            results = df[df['full_line'].str.contains(search, case=False, na=False)]
            st.write(f"تم العثور على {len(results)} كلمة:")
            for item in results['full_line']:
                st.write(f"✅ {item}")
        else:
            st.write("كل الكلمات:")
            st.table(df) # يعرض القائمة كاملة كجدول
else:
    st.error("تأكد أن ملف vocab.csv موجود في GitHub")
        
