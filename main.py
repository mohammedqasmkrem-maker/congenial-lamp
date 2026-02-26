import streamlit as st
import pandas as pd
import random
import os
import time

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="أكاديمية اللغة", layout="wide")

# تصميم CSS لجعل المربعات في الوسط وشكلها جذاب
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 15px; height: 100px; font-size: 24px; font-weight: bold; border: 2px solid #007bff; }
    .stButton>button:hover { background-color: #007bff; color: white; }
    .card { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }
    .stat-box { background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات والحالة
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "home"
if 'prizes' not in st.session_state: st.session_state.prizes = []

@st.cache_data
def load_data():
    if os.path.exists('vocab.csv'):
        return pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    return pd.DataFrame({'full_line': ['Apple - تفاحة', 'Smart - ذكي', 'Success - نجاح']})

df = load_data()

# 3. محتوى الصفحات
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #007bff;'>👋 أهلاً بك في الأكاديمية الذكية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>اختر طريقك اليوم نحو الاحتراف</p>", unsafe_allow_html=True)
    
    st.write("##")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎮 ابدأ التحدي\n(30 ثانية)"):
            st.session_state.page = "challenge"
            st.session_state.start_time = time.time()
            st.rerun()
            
    with col2:
        if st.button("📖 القاموس\nالبحث السريع"):
            st.session_state.page = "dictionary"
            st.rerun()
    
    st.write("---")
    # قسم الإعدادات والإحصائيات
    with st.expander("⚙️ إحصائياتك وجوائزك (اضغط هنا)"):
        c1, c2, c3 = st.columns(3)
        c1.metric("نقاطك الحالية 🏆", st.session_state.score)
        c2.write("**الجوائز التي ربحتها:**")
        if st.session_state.prizes:
            for p in st.session_state.prizes: st.write(f"- {p}")
        else: st.write("لا توجد جوائز بعد. ابدأ اللعب!")
        
        # تحديد المرحلة
        stage = "مبتدأ 🌱"
        if st.session_state.score > 100: stage = "مكافح ⚡"
        if st.session_state.score > 500: stage = "محترف 🔥"
        c3.metric("مرحلتك الحالية", stage)

elif st.session_state.page == "challenge":
    st.title("🎯 تحدي الـ 30 ثانية")
    
    # حساب الوقت
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 30 - int(elapsed))
    
    st.progress(rem / 30)
    st.subheader(f"⏳ الوقت المتبقي: {rem} ثانية")
    
    if 'current_q' not in st.session_state or st.session_state.get('next_q', True):
        st.session_state.current_q = random.choice(df['full_line'].values)
        st.session_state.next_q = False

    q = st.session_state.current_q
    eng, arb = q.split('-')[0].strip(), q.split('-')[1].strip()
    
    st.info(f"ما معنى كلمة: **{eng}**؟")
    ans = st.text_input("اكتب الحل واضغط Enter:").strip()
    
    if ans == arb and rem > 0:
        st.success("إجابة صحيحة! +20 نقطة")
        st.session_state.score += 20
        # نظام الجوائز
        if st.session_state.score % 100 == 0:
            st.session_state.prizes.append(f"وسام الـ {st.session_state.score} نقطة 🎖️")
            st.balloons()
        st.session_state.next_q = True
        time.sleep(1)
        st.rerun()
    elif rem == 0:
        st.error("انتهى الوقت!")
        if st.button("العودة للقائمة"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "dictionary":
    st.title("📖 القاموس")
    if st.button("⬅️ عودة"): st.session_state.page = "home"; st.rerun()
    search = st.text_input("🔍 ابحث عن أي كلمة:")
    if search:
        st.table(df[df['full_line'].str.contains(search, case=False)])

# 4. الروابط في أسفل الشاشة
st.markdown("---")
st.markdown("<p style='text-align: center;'>📢 شارك التطبيق مع أصدقائك</p>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("[✈️ تليجرام](https://t.me/share/url?url=YOUR_URL&text=جرب_تحدي_اللغة)")
with col_b:
    st.markdown("[🟢 واتساب](https://api.whatsapp.com/send?text=جرب_تحدي_اللغة)")
    
