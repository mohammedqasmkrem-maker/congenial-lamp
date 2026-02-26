import streamlit as st
import pandas as pd
import random

# إعدادات الصفحة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide", page_icon="🎓")

# 1. دالة تحميل البيانات وتقسيم المستويات
@st.cache_data
def load_data():
    try:
        # قراءة الملف (الرقم والكلمة والترجمة) كسطر واحد
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
        # تقسيم المستويات تلقائياً
        df['level'] = 'سهل'
        df.loc[300:700, 'level'] = 'متوسط'
        df.loc[700:, 'level'] = 'صعب'
        return df
    except:
        return None

df = load_data()

# 2. القائمة الجانبية (التقييم والمشاركة)
st.sidebar.title("📊 لوحة التحكم")

# نظام التقييم بالنجوم
st.sidebar.subheader("⭐ قيم تجربتك")
star_rating = st.sidebar.select_slider("اختر النجوم:", options=[1, 2, 3, 4, 5], value=5)
if st.sidebar.button("إرسال التقييم"):
    st.sidebar.success(f"شكراً! تم تسجيل {star_rating} نجوم")

st.sidebar.markdown("---")

# زر المشاركة عبر الواتساب
st.sidebar.subheader("📢 انشر التطبيق")
app_url = "https://your-app-link.streamlit.app" # استبدل هذا برابط تطبيقك من شريط المتصفح
share_msg = f"تعال جرب 'أكاديمية الـ 1000 كلمة'.. تطبيق رهيب لتعلم الإنجليزية! {app_url}"
whatsapp_link = f"https://wa.me/?text={share_msg}"
st.sidebar.markdown(f'[📲 مشاركة عبر الواتساب]({whatsapp_link})')

st.sidebar.markdown("---")
menu = st.sidebar.radio("انتقل إلى:", ["🎯 تحدي المستويات", "📖 القاموس الذكي"])

# 3. محتوى التطبيق
if df is not None:
    if menu == "🎯 تحدي المستويات":
        st.title("🎯 تحدي الـ 1000 كلمة")
        st.write("اختر مستواك وابدأ التحدي!")
        
        level_choice = st.selectbox("اختر الصعوبة:", ["سهل", "متوسط", "صعب"])
        filtered_words = df[df['level'] == level_choice]

        if st.button("توليد كلمة جديدة 🔄"):
            st.session_state.current_item = random.choice(filtered_words['full_line'].values)
            st.session_state.show_res = False

        if 'current_item' in st.session_state:
            item = st.session_state.current_item
            # عرض الجزء الأول قبل النقطة أو الداش للتشويق
            display_word = item.split('-')[0] if '-' in item else item.split('.')[0]
            
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="color: #0e1117;">{display_word}</h1>
            </div>
            """, unsafe_allow_html=True)

            if st.button("👁️ إظهار الحل"):
                st.session_state.show_res = True
            
            if st.session_state.get('show_res'):
                st.success(f"### النتيجة كاملة: \n {item}")

    elif menu == "📖 القاموس الذكي":
        st.title("📖 القاموس المصنف")
        search = st.text_input("🔍 ابحث عن أي كلمة (عربي أو إنجليزي):")
        
        selected_levels = st.multiselect("تصفية حسب المستوى:", ["سهل", "متوسط", "صعب"], default=["سهل", "متوسط", "صعب"])
        
        display_df = df[df['level'].isin(selected_levels)]
        
        if search:
            display_df = display_df[display_df['full_line'].str.contains(search, case=False)]
        
        st.dataframe(display_df[['level', 'full_line']], use_container_width=True, height=600)

else:
    st.error("❌ خطأ: لم نجد ملف vocab.csv في مستودع GitHub الخاص بك.")
    
