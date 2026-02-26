import streamlit as st
import pandas as pd
import random
import os
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide", page_icon="🎓")

# دالة تحميل البيانات
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

# --- القائمة الجانبية (المشاركة والتقييم) ---
st.sidebar.title("📊 الإحصائيات والمشاركة")

# رابط التطبيق (تأكد من وضع رابطك الحقيقي هنا)
my_app_url = "https://your-app-link.streamlit.app" 
share_text = f"جرب تحدي الكتابة في تطبيق 'أكاديمية الـ 1000 كلمة'! 🚀\n{my_app_url}"
encoded_text = urllib.parse.quote(share_text)

# أزرار المشاركة
st.sidebar.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)](https://wa.me/?text={encoded_text})")
st.sidebar.markdown(f"[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat&logo=telegram&logoColor=white)](https://t.me/share/url?url={my_app_url}&text={encoded_text})")

st.sidebar.markdown("---")
menu = st.sidebar.radio("انتقل إلى:", ["🎯 تحدي الكتابة", "📖 القاموس الشامل"])

# --- محتوى التطبيق ---
if df is not None:
    if menu == "🎯 تحدي الكتابة":
        st.title("🎯 اختبر إملاءك وحفظك")
        lvl = st.selectbox("اختر المستوى:", ["سهل", "متوسط", "صعب"])
        level_df = df[df['level'] == lvl]
        
        if st.sidebar.button("🔄 كلمة جديدة"):
            st.session_state.word_data = random.choice(level_df['full_line'].values)
            st.session_state.answer_correct = None
            st.rerun()

        if 'word_data' not in st.session_state:
            st.session_state.word_data = random.choice(level_df['full_line'].values)

        # تحضير السؤال والجواب
        # نفترض السطر بصيغة: Apple - تفاحة
        full_word = st.session_state.word_data
        english_part = full_word.split('-')[0].strip() if '-' in full_word else full_word
        arabic_part = full_word.split('-')[1].strip() if '-' in full_word else "خمن الكلمة"

        st.info(f"### ما معنى كلمة: **{arabic_part}** بالإنجليزية؟")
        
        user_answer = st.text_input("اكتب الكلمة هنا بالإنجليزية:", key="user_input").strip()

        if st.button("تحقق من الإجابة ✅"):
            if user_answer.lower() == english_part.lower():
                st.success(f"ممتاز! إجابة صحيحة: **{english_part}** 🎉")
            else:
                st.error(f"للأسف خطأ! الإجابة الصحيحة هي: **{english_part}**")
                st.info(f"أنت كتبت: {user_answer}")

    elif menu == "📖 القاموس الشامل":
        st.title("📖 قاموس الـ 1000 كلمة")
        search = st.text_input("🔍 ابحث (عربي/إنجليزي):")
        filtered = df[df['full_line'].str.contains(search, case=False)] if search else df
        st.dataframe(filtered[['level', 'full_line']], use_container_width=True)

else:
    st.error("⚠️ ملف 'vocab.csv' غير موجود في GitHub بنفس الاسم.")
    
