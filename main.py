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

# --- القائمة الجانبية المحدثة ---
st.sidebar.title("📊 مركز التحكم")

# نظام التقييم
st.sidebar.subheader("⭐ تقييمك يهمنا")
rating = st.sidebar.select_slider("النجوم:", options=[1, 2, 3, 4, 5], value=5)
if st.sidebar.button("حفظ التقييم"):
    st.sidebar.success("شكراً لك!")

st.sidebar.markdown("---")

# --- قسم المشاركة لكل التطبيقات ---
st.sidebar.subheader("📢 انشر في كل مكان")

# ملاحظة: ضع رابطك الحقيقي هنا
my_app_url = "https://your-app-link.streamlit.app" 
share_text = f"جرب تطبيق 'أكاديمية الـ 1000 كلمة' لتعلم الإنجليزية مجاناً وتحدي نفسك! 🚀\n{my_app_url}"
encoded_text = urllib.parse.quote(share_text)

# روابط المشاركة
col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)](https://wa.me/?text={encoded_text})")
    st.markdown(f"[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat&logo=telegram&logoColor=white)](https://t.me/share/url?url={my_app_url}&text={encoded_text})")
with col2:
    st.markdown(f"[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=flat&logo=facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?u={my_app_url})")
    st.markdown(f"[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/intent/tweet?text={encoded_text})")

st.sidebar.markdown("---")
menu = st.sidebar.radio("القائمة:", ["🎯 التحدي الذكي", "📖 القاموس الشامل"])

# --- محتوى التطبيق ---
if df is not None:
    if menu == "🎯 التحدي الذكي":
        st.title("🎯 تحدي الـ 1000 كلمة")
        lvl = st.selectbox("اختر المستوى:", ["سهل", "متوسط", "صعب"])
        level_df = df[df['level'] == lvl]
        
        if st.button("كلمة جديدة 🔄") or 'current_word' not in st.session_state:
            if not level_df.empty:
                st.session_state.current_word = random.choice(level_df['full_line'].values)
                st.session_state.reveal = False

        if 'current_word' in st.session_state:
            word = st.session_state.current_word
            clean_word = word.split('-')[0] if '-' in word else word
            st.info(f"### خمن معنى: \n # {clean_word}")
            if st.button("👀 إظهار الحل"): st.session_state.reveal = True
            if st.session_state.get('reveal'): st.success(f"### {word}")

    elif menu == "📖 القاموس الشامل":
        st.title("📖 قاموس الأكاديمية")
        search = st.text_input("🔍 ابحث عن كلمة:")
        filtered = df[df['full_line'].str.contains(search, case=False)] if search else df
        st.dataframe(filtered[['level', 'full_line']], use_container_width=True)
else:
    st.error("⚠️ ملف 'vocab.csv' غير موجود في GitHub بنفس الاسم.")
        
