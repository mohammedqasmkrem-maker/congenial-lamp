import streamlit as st
import pandas as pd
import random

# إعدادات الصفحة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="centered")

@st.cache_data
def load_data():
    return pd.read_csv('vocab.csv', header=None, names=['full_text'])

try:
    df = load_data()
    
    # القائمة الجانبية للتنقل
    st.sidebar.title("📌 القائمة الرئيسية")
    choice = st.sidebar.radio("اختر ماذا تريد أن تفعل:", ["🎯 اختبار ذكي", "📖 قاموس الكلمات (تعلم)"])

    if choice == "🎯 اختبار ذكي":
        st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🧠 تحدي الذاكرة</h1>", unsafe_content=True)
        st.write("---")
        
        if 'test_word' not in st.session_state:
            st.session_state.test_word = random.choice(df['full_text'].values)
            st.session_state.revealed = False

        # عرض الكلمة فقط (بدون الترجمة)
        word_only = st.session_state.test_word.split('.')[1].strip().split(' ')[0] if '.' in st.session_state.test_word else "كلمة جديدة"
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 40px; border-radius: 20px; text-align: center; border: 4px solid #FF4B4B;">
            <h3 style="color: white;">ما معنى هذه الكلمة؟</h3>
            <h1 style="color: #FF4B4B; font-size: 60px;">{word_only}</h1>
        </div>
        """, unsafe_content=True)

        if st.button("كشف الإجابة والترجمة ✨", use_container_width=True):
            st.session_state.revealed = True

        if st.session_state.revealed:
            st.balloons()
            st.success(f"✅ الحل الصحيح هو: **{st.session_state.test_word}**")
            if st.button("كلمة تالية ➡️", use_container_width=True):
                st.session_state.test_word = random.choice(df['full_text'].values)
                st.session_state.revealed = False
                st.rerun()

    else: # وضع القاموس
        st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📖 قاموس التعلم الذاتي</h1>", unsafe_content=True)
        st.info("تصفح الكلمات الـ 1000 واحفظها واحدة تلو الأخرى")
        st.write("---")
        
        search_query = st.text_input("🔍 ابحث عن كلمة معينة:")
        filtered_df = df[df['full_text'].str.contains(search_query, case=False)] if search_query else df

        for index, row in filtered_df.head(20).iterrows():
            st.markdown(f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid #4CAF50;">
                <p style="color: #333; font-size: 20px; margin: 0;">{row['full_text']}</p>
            </div>
            """, unsafe_content=True)
        
        if len(filtered_df) > 20:
            st.caption(f"يتم عرض أول 20 كلمة فقط من أصل {len(filtered_df)}")

except Exception as e:
    st.error("تأكد من وجود ملف vocab.csv في حسابك")
        
