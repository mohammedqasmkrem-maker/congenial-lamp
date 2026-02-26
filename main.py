import streamlit as st
import pandas as pd
import random
import os
import urllib.parse
import time

# 1. إعدادات احترافية للصفحة
st.set_page_config(page_title="أكاديمية اللغة الإنجليزية", layout="wide", page_icon="🚀")

# تنسيق CSS لجعل الواجهة تبدو كتطبيق موبايل احترافي
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 15px; text-align: center; font-size: 20px; }
    .score-box { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 2px solid #007bff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات وتصنيف المستويات
@st.cache_data
def load_data():
    file_name = 'vocab.csv'
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name, header=None, names=['full_line'], sep='|', engine='python')
            df['level'] = 'سهل 🌱'
            if len(df) > 300: df.loc[300:700, 'level'] = 'متوسط ⚡'
            if len(df) > 700: df.loc[700:, 'level'] = 'صعب 🔥'
            return df
        except: return None
    return None

df = load_data()

# 3. إدارة الحالة (Session State)
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state: st.session_state.current_word = None
if 'answered' not in st.session_state: st.session_state.answered = False

# 4. القائمة الجانبية (Sidebar) - مثل التطبيقات الكبرى
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=100)
st.sidebar.title("لوحة الصدارة")
st.sidebar.markdown(f"""
<div class="score-box">
    <h3>نقاطك الإجمالية</h3>
    <h1 style="color: #007bff;">{st.session_state.score}</h1>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
# أزرار مشاركة احترافية
app_url = "https://your-app-link.streamlit.app" # ضع رابطك هنا
encoded_msg = urllib.parse.quote(f"تحديت نفسي في تطبيق تعلم الإنجليزية وجمعت {st.session_state.score} نقطة! 🏆\nجربه الآن: {app_url}")
st.sidebar.subheader("📢 تحدَّ أصدقاءك")
st.sidebar.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-Share-25D366?style=for-the-badge&logo=whatsapp)](https://wa.me/?text={encoded_msg})")

menu = st.sidebar.radio("الوضع الحالي:", ["🎮 تحدي الذكاء", "📖 القاموس الذكي", "📈 إحصائياتي"])

# 5. محتوى التطبيق الرئيسي
if df is not None:
    if menu == "🎮 تحدي الذكاء":
        st.title("🎮 وضع التحدي التفاعلي")
        
        col1, col2 = st.columns([2, 1])
        with col2:
            lvl = st.selectbox("اختر مستواك:", ["سهل 🌱", "متوسط ⚡", "صعب 🔥"])
        
        level_df = df[df['level'] == lvl]

        # اختيار كلمة جديدة
        if st.button("توليد كلمة جديدة 🔄") or st.session_state.current_word is None:
            st.session_state.current_word = random.choice(level_df['full_line'].values)
            st.session_state.answered = False
            st.rerun()

        word_data = st.session_state.current_word
        eng = word_data.split('-')[0].strip() if '-' in word_data else word_data
        arb = word_data.split('-')[1].strip() if '-' in word_data else "غير معروف"

        st.markdown(f"<h2 style='text-align: center;'>ترجم الكلمة التالية إلى العربية:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: #007bff;'>{eng}</h1>", unsafe_allow_html=True)

        user_input = st.text_input("أدخل المعنى بالعربي هنا...", key="user_input").strip()

        if st.button("تأكيد الإجابة ✅"):
            if user_input == arb:
                st.balloons()
                st.success(f"إجابة عبقرية! 🎉 الكلمة هي: {arb}")
                st.session_state.score += 20
                st.session_state.answered = True
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"للأسف خطأ! المعنى الصحيح هو: {arb}")
                st.session_state.score = max(0, st.session_state.score - 5) # خصم نقاط عند الخطأ
                st.info("حاول مرة أخرى مع كلمة جديدة لتعويض النقاط!")

    elif menu == "📖 القاموس الذكي":
        st.title("📖 القاموس الشامل")
        search = st.text_input("🔍 ابحث عن أي كلمة بالإنجليزية أو العربية...")
        filtered = df[df['full_line'].str.contains(search, case=False)] if search else df
        st.dataframe(filtered[['level', 'full_line']], use_container_width=True, height=500)

    elif menu == "📈 إحصائياتي":
        st.title("📈 تقدمك الدراسي")
        st.write(f"لقد قمت بمراجعة الكثير من الكلمات اليوم!")
        st.progress(min(st.session_state.score / 1000, 1.0))
        st.write(f"أنت الآن تمتلك {st.session_state.score} نقطة خبرة.")

else:
    st.error("⚠️ ملف vocab.csv مفقود! ارفعه على GitHub ليعمل التطبيق.")
