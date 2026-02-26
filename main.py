import streamlit as st
import pandas as pd
import random
import os
import time
import urllib.parse

# 1. إعدادات الصفحة (تجعلها تعمل كـ تطبيق موبايل)
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide")

# 2. وظيفة تحميل الكلمات (ضمان العمل حتى بدون ملف خارجي)
@st.cache_data
def load_data():
    file_path = 'vocab.csv'
    if os.path.exists(file_path):
        try:
            # محاولة قراءة ملفك
            df = pd.read_csv(file_path, header=None, names=['full_line'], sep='|', engine='python')
            return df
        except:
            pass
    
    # إذا لم يجد الملف، يستخدم هذه الكلمات لكي "يشتغل" التطبيق ولا يبقى صورة
    return pd.DataFrame({'full_line': [
        'Apple - تفاحة', 'Smart - ذكي', 'Success - نجاح', 
        'School - مدرسة', 'Book - كتاب', 'Water - ماء'
    ]})

df = load_data()

# إدارة النقاط والصفحات
if 'score' not in st.session_state: st.session_state.score = 0
if 'prizes' not in st.session_state: st.session_state.prizes = []

# --- 3. القائمة الجانبية (Sidebar) للتنقل الفعلي ---
with st.sidebar:
    st.header("🎮 لوحة التحكم")
    menu = st.radio("انتقل إلى الصفحات:", 
                    ["🏠 الرئيسية", "🎯 التحدي (30 ثانية)", "📖 البحث في القاموس", "🏆 إنجازاتي"])
    
    st.write("---")
    st.metric("نقاطك الحالية", st.session_state.score)
    
    # روابط المشاركة المباشرة
    st.subheader("📢 انشر التطبيق")
    app_url = "https://mohammedqasmkrem-maker.streamlit.app"
    msg = urllib.parse.quote(f"تحدي الـ 1000 كلمة! جرب مستواك معي: {app_url}")
    st.markdown(f"[🟢 واتساب](https://api.whatsapp.com/send?text={msg})")
    st.markdown(f"[✈️ تليجرام](https://t.me/share/url?url={app_url}&text={msg})")

# --- 4. تشغيل الصفحات (المحتوى التفاعلي) ---

if menu == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center;'>👋 أهلاً بك في تطبيقك الشغال</h1>", unsafe_allow_html=True)
    st.info("اختر 'التحدي' من القائمة الجانبية لتبدأ اللعب، أو 'القاموس' للبحث.")
    st.success(f"لديك الآن {len(df)} كلمة جاهزة للاختبار!")

elif menu == "🎯 التحدي (30 ثانية)":
    st.title("🎯 ابدأ الاختبار الآن")
    
    if st.button("كلمة جديدة 🔄") or 'word_to_guess' not in st.session_state:
        st.session_state.word_to_guess = random.choice(df['full_line'].values)
        st.session_state.start_t = time.time()
        st.session_state.checked = False
        st.rerun()

    # المؤقت الحقيقي
    rem = max(0, 30 - int(time.time() - st.session_state.start_t))
    st.progress(rem / 30)
    st.write(f"⏳ الوقت المتبقي: {rem} ثانية")

    if rem == 0:
        st.error("⏰ انتهى الوقت! اضغط 'كلمة جديدة'")
    else:
        line = st.session_state.word_to_guess
        eng = line.split('-')[0].strip()
        arb = line.split('-')[1].strip() if '-' in line else "غير مترجم"
        
        st.subheader(f"ما معنى الكلمة: {eng}؟")
        ans = st.text_input("اكتب الحل بالعربي:").strip()
        
        if st.button("تحقق ✅"):
            if ans == arb:
                st.success("إجابة صحيحة! +20 نقطة")
                st.session_state.score += 20
                if st.session_state.score % 100 == 0:
                    st.session_state.prizes.append(f"وسام الـ {st.session_state.score} 🎖️")
                    st.balloons()
            else:
                st.error(f"خطأ! الجواب هو: {arb}")

elif menu == "📖 البحث في القاموس":
    st.title("📖 القاموس التفاعلي")
    query = st.text_input("🔍 ابحث عن كلمة:")
    if query:
        results = df[df['full_line'].str.contains(query, case=False)]
        st.table(results)
    else:
        st.write("اكتب شيئاً للبحث عنه...")

elif menu == "🏆 إنجازاتي":
    st.title("🏆 لوحة الشرف")
    st.write(f"مجموع نقاطك: {st.session_state.score}")
    if st.session_state.prizes:
        for p in st.session_state.prizes:
            st.success(p)
    else:
        st.write("لم تحصل على جوائز بعد.")
    
