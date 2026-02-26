import streamlit as st
import pandas as pd
import random

# إعداد الصفحة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide")

# دالة تحميل البيانات
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
        # إضافة عمود المستوى تلقائياً بناءً على ترتيب الكلمات
        df['level'] = 'سهل'
        df.loc[300:700, 'level'] = 'متوسط'
        df.loc[700:, 'level'] = 'صعب'
        return df
    except:
        return None

df = load_data()

# --- القائمة الجانبية (الإحصائيات والتقييم) ---
st.sidebar.title("📊 إحصائيات وتقييم")
if 'visitors' not in st.session_state:
    st.session_state.visitors = random.randint(150, 250)
else:
    st.session_state.visitors += 1

st.sidebar.metric("👥 عدد المستفيدين", f"{st.session_state.visitors}+")

# نظام التقييم
st.sidebar.markdown("---")
st.sidebar.subheader("⭐ قيم الأكاديمية")
rating = st.sidebar.slider("النجوم:", 1, 5, 5)
if st.sidebar.button("إرسال التقييم"):
    st.sidebar.success("شكراً لتقييمك!")

# --- الأقسام الرئيسية ---
st.sidebar.markdown("---")
menu = st.sidebar.radio("انتقل إلى:", ["🎯 التحدي بالمستويات", "📖 القاموس المرتب"])

if df is not None:
    if menu == "🎯 التحدي بالمستويات":
        st.title("🎯 تحدي المستويات")
        selected_level = st.selectbox("اختر مستوى الصعوبة:", ["سهل", "متوسط", "صعب"])
        
        # تصفية الكلمات حسب المستوى المختار
        level_df = df[df['level'] == selected_level]
        
        if st.button("توليد كلمة جديدة"):
            st.session_state.current_word = random.choice(level_df['full_line'].values)
            st.session_state.revealed = False

        if 'current_word' in st.session_state:
            raw_word = st.session_state.current_word
            english_only = raw_word.split('-')[0] if '-' in raw_word else raw_word
            
            st.info(f"### المستوى: {selected_level} \n # الكلمة: {english_only}")

            if st.button("👀 إظهار الحل"):
                st.session_state.revealed = True
            
            if st.session_state.get('revealed'):
                st.success(f"### الترجمة: {st.session_state.current_word}")

    elif menu == "📖 القاموس المرتب":
        st.title("📖 القاموس المصنف")
        level_choice = st.multiselect("عرض مستويات محددة:", ["سهل", "متوسط", "صعب"], default=["سهل", "متوسط", "صعب"])
        
        search = st.text_input("🔍 ابحث عن كلمة محددة:")
        
        # تصفية الجدول
        filtered_df = df[df['level'].isin(level_choice)]
        if search:
            filtered_df = filtered_df[filtered_df['full_line'].str.contains(search, case=False)]
            
        st.dataframe(filtered_df[['level', 'full_line']], use_container_width=True, height=500)

else:
    st.error("تأكد من وجود ملف vocab.csv في GitHub")
        
