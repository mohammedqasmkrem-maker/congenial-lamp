import streamlit as st
import pandas as pd
import random

# إعدادات الواجهة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide")

# دالة تحميل البيانات بشكل صحيح
@st.cache_data
def load_data():
    try:
        # نقرأ السطر كاملاً مهما كان محتواه
        df = pd.read_csv('vocab.csv', header=None, names=['full_text'])
        return df
    except:
        return None

df = load_data()

# إضافة القائمة الجانبية (القاموس + الاختبار)
st.sidebar.title("🚀 لوحة التحكم")
page = st.sidebar.radio("انتقل إلى:", ["🎯 اختبار التحدي", "📖 القاموس الشامل"])

if df is not None:
    if page == "🎯 اختبار التحدي":
        st.title("🎯 تحدي الـ 1000 كلمة")
        
        if 'current_item' not in st.session_state:
            st.session_state.current_item = random.choice(df['full_text'].values)
            st.session_state.revealed = False

        # صندوق عرض الكلمة
        st.markdown(f"""
        <div style="background-color: #1e2b3c; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #3e4b5c;">
            <h2 style="color: white; margin-bottom: 10px;">ما معنى هذه الكلمة؟</h2>
        </div>
        """, unsafe_allow_html=True)

        # عرض الكلمة (نتجنب عرض الرقم فقط هنا)
        raw_text = st.session_state.current_item
        st.info(f"### {raw_text.split('.')[0]} ...") # عرض بداية السطر للتشويق

        if st.button("👀 إظهار الكلمة والترجمة"):
            st.session_state.revealed = True
        
        if st.session_state.revealed:
            st.success(f"### ✨ {st.session_state.current_item}")
            if st.button("➡️ الكلمة التالية"):
                st.session_state.current_item = random.choice(df['full_text'].values)
                st.session_state.revealed = False
                st.rerun()

    elif page == "📖 القاموس الشامل":
        st.title("📖 قاموس الأكاديمية")
        search = st.text_input("🔍 ابحث عن كلمة (بالعربي أو الإنجليزي):")
        
        # تصفية الكلمات بناءً على البحث
        if search:
            results = df[df['full_text'].str.contains(search, case=False, na=False)]
            st.write(f"نتائج البحث ({len(results)}):")
            for item in results['full_text']:
                st.write(f"🔹 {item}")
        else:
            st.write("استعرض قائمة الـ 1000 كلمة:")
            st.dataframe(df, use_container_width=True, height=400)

else:
    st.error("لم نجد ملف vocab.csv. تأكد من رفعه على GitHub.")
            
