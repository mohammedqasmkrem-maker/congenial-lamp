import streamlit as st
import pandas as pd
import random
import os
import time
import urllib.parse

# 1. إعدادات الصفحة والتصميم (CSS)
st.set_page_config(page_title="أكاديمية اللغة الإنجليزية", layout="wide")

st.markdown("""
    <style>
    /* تنسيق الحاوية الرئيسية */
    .stApp { background-color: #f8f9fa; }
    
    /* تنسيق الأزرار الكبيرة في المنتصف */
    .big-button {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: white;
        border: 2px solid #007bff;
        border-radius: 20px;
        padding: 40px;
        margin: 10px;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .big-button:hover {
        background-color: #007bff;
        color: white;
        transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات والنظام
if 'page' not in st.session_state: st.session_state.page = "home"
if 'score' not in st.session_state: st.session_state.score = 0
if 'prizes' not in st.session_state: st.session_state.prizes = []

def load_data():
    if os.path.exists('vocab.csv'):
        return pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    return pd.DataFrame({'full_line': ['Apple - تفاحة', 'Smart - ذكي', 'Success - نجاح']})

df = load_data()

# 3. محتوى الصفحات
# --- صفحة الترحيب والاختيار ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #007bff;'>👋 أهلاً بك في الأكاديمية!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>اختر القسم الذي تريد البدء به:</p>", unsafe_allow_html=True)
    
    st.write("##")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎮 تحدي الـ 30 ثانية\n(ابدأ المسابقة)"):
            st.session_state.page = "game"
            st.session_state.start_time = time.time()
            st.rerun()
            
    with col2:
        if st.button("📖 القاموس الذكي\n(ابحث عن الكلمات)"):
            st.session_state.page = "dict"
            st.rerun()
    
    st.write("---")
    # قسم الإعدادات والجوائز
    with st.expander("⚙️ إحصائياتك وجوائزك"):
        c1, c2 = st.columns(2)
        c1.metric("نقاطك الحالية", st.session_state.score)
        stage = "مبتدئ 🌱" if st.session_state.score < 100 else "محترف 🔥"
        c2.metric("المستوى", stage)
        st.write("**الأوسمة والجوائز:**")
        if not st.session_state.prizes: st.write("لم تحصل على جوائز بعد. اجتهد أكثر!")
        else: st.write(", ".join(st.session_state.prizes))

# --- صفحة التحدي ---
elif st.session_state.page == "game":
    st.title("🎯 تحدي السرعة (30 ثانية)")
    
    # العداد الزمني
    rem = max(0, 30 - int(time.time() - st.session_state.start_time))
    st.progress(rem / 30)
    st.subheader(f"⏳ الوقت المتبقي: {rem} ثانية")
    
    if rem == 0:
        st.error("⏰ انتهى الوقت!")
        if st.button("العودة للرئيسية"): st.session_state.page = "home"; st.rerun()
    else:
        if 'q' not in st.session_state or st.session_state.get('new_q', True):
            st.session_state.q = random.choice(df['full_line'].values)
            st.session_state.new_q = False
        
        eng = st.session_state.q.split('-')[0].strip()
        arb = st.session_state.q.split('-')[1].strip()
        
        st.info(f"ما معنى: **{eng}**؟")
        ans = st.text_input("اكتب الجواب بالعربي:").strip()
        
        if st.button("تحقق ✅"):
            if ans == arb:
                st.success("إجابة صحيحة! +20 نقطة")
                st.session_state.score += 20
                if st.session_state.score % 100 == 0:
                    st.session_state.prizes.append(f"وسام الـ {st.session_state.score} 🎖️")
                    st.balloons()
                st.session_state.new_q = True
                st.rerun()
            else:
                st.error(f"خطأ! الجواب هو: {arb}")

# --- صفحة القاموس ---
elif st.session_state.page == "dict":
    st.title("📖 القاموس والبحث")
    if st.button("⬅️ عودة"): st.session_state.page = "home"; st.rerun()
    
    search = st.text_input("🔍 اكتب الكلمة للبحث (عربي أو إنجليزي):")
    if search:
        res = df[df['full_line'].str.contains(search, case=False)]
        st.table(res)
    else:
        st.write("جميع الكلمات:")
        st.dataframe(df, use_container_width=True)

# 4. روابط المشاركة (أسفل الشاشة دائماً)
st.markdown("---")
st.markdown("<p style='text-align: center;'>📢 انشر العلم وشارك التطبيق</p>", unsafe_allow_html=True)
my_url = "https://your-app-link.streamlit.app"
encoded_text = urllib.parse.quote(f"تحدي الـ 1000 كلمة! جرب مستواك معي: {my_url}")

c_left, c_right = st.columns(2)
with c_left:
    st.markdown(f"[![واتساب](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://api.whatsapp.com/send?text={encoded_text})", unsafe_allow_html=True)
with c_right:
    st.markdown(f"[![تليجرام](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/share/url?url={my_url}&text={encoded_text})", unsafe_allow_html=True)
