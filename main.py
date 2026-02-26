import streamlit as st
import pandas as pd
import random
import os
import time
import urllib.parse

# إعداد الصفحة
st.set_page_config(page_title="أكاديمية اللغة", layout="wide")

# إدارة الحالة والنقاط
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "home"
if 'prizes' not in st.session_state: st.session_state.prizes = []

# تحميل البيانات
def load_data():
    if os.path.exists('vocab.csv'):
        return pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    return pd.DataFrame({'full_line': ['Apple - تفاحة', 'Smart - ذكي', 'Success - نجاح']})

df = load_data()

# --- الواجهة الرئيسية (تظهر فوراً) ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #007bff;'>👋 أهلاً بك في الأكاديمية!</h1>", unsafe_allow_html=True)
    st.write("##")
    
    # مربعات الاختيار في وسط الشاشة
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 ابدأ التحدي\n(30 ثانية)", use_container_width=True):
            st.session_state.page = "game"
            st.session_state.start_time = time.time()
            st.rerun()
    with col2:
        if st.button("📖 القاموس\n(البحث السريع)", use_container_width=True):
            st.session_state.page = "dict"
            st.rerun()
            
    # قسم الجوائز والإحصائيات
    st.write("---")
    with st.expander("⚙️ إحصائياتك وجوائزك"):
        c1, c2 = st.columns(2)
        c1.metric("نقاطك الحالية 🏆", st.session_state.score)
        stage = "مبتدئ 🌱" if st.session_state.score < 100 else "محترف 🔥"
        c2.metric("المرحلة", stage)
        st.write("**الأوسمة:** " + (", ".join(st.session_state.prizes) if st.session_state.prizes else "لا توجد بعد"))

elif st.session_state.page == "game":
    st.title("🎯 تحدي الـ 30 ثانية")
    rem = max(0, 30 - int(time.time() - st.session_state.start_time))
    st.progress(rem / 30)
    st.subheader(f"⏳ الوقت المتبقي: {rem} ثانية")
    
    if rem == 0:
        st.error("⏰ انتهى الوقت!")
        if st.button("العودة للقائمة الرئيسية"): st.session_state.page = "home"; st.rerun()
    else:
        # (هنا يوضع كود السؤال والجواب الذي برمجناه سابقاً)
        st.info("اكتب معنى الكلمة التي تظهر لك!")

elif st.session_state.page == "dict":
    st.title("📖 القاموس الذكي")
    if st.button("⬅️ عودة"): st.session_state.page = "home"; st.rerun()
    search = st.text_input("🔍 ابحث عن كلمة:")
    if search:
        st.table(df[df['full_line'].str.contains(search, case=False)])

# --- قسم روابط المشاركة (أسفل الشاشة) ---
st.write("---")
st.markdown("<p style='text-align: center;'>📢 انشر التحدي مع أصدقائك</p>", unsafe_allow_html=True)

# هذا الكود سيجلب رابط تطبيقك الحقيقي تلقائياً
# إذا لم يعمل التلقائي، استبدل الرابط أدناه برابطك من المتصفح
real_app_url = "https://mohammedqasmkrem-maker.streamlit.app" 
share_text = urllib.parse.quote(f"تحديت نفسي في أكاديمية الـ 1000 كلمة! جرب مستواك معي: {real_app_url}")

c_wa, c_tg = st.columns(2)
with c_wa:
    st.markdown(f"[![واتساب](https://img.shields.io/badge/WhatsApp-Share-25D366?style=for-the-badge&logo=whatsapp)](https://api.whatsapp.com/send?text={share_text})", unsafe_allow_html=True)
with c_tg:
    st.markdown(f"[![تليجرام](https://img.shields.io/badge/Telegram-Share-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/share/url?url={real_app_url}&text={share_text})", unsafe_allow_html=True)
