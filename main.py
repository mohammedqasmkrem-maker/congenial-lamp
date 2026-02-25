import streamlit as st
import pandas as pd
import random

# إعدادات واجهة التطبيق
st.set_page_config(page_title="تحدي الـ 1000 كلمة", layout="centered")

# دالة تحميل ملف الكلمات
@st.cache_data
def load_data():
    # هنا الكود يقرأ الملف بالاسم السهل اللي اختاريته
    return pd.read_csv('1000_english_words-3.txt')

try:
    df = load_data()
    
    st.title("🎓 تطبيق حفظ 1000 كلمة")
    st.write("اختبر معلوماتك في اللغة الإنجليزية!")
    st.divider()

    # تهيئة العدادات في ذاكرة المتصفح
    if 'score' not in st.session_state: st.session_state.score = 0
    if 'count' not in st.session_state: st.session_state.count = 0

    # اختيار كلمة عشوائية
    if 'current_word' not in st.session_state:
        st.session_state.current_word = df.sample(1).iloc[0]

    word = st.session_state.current_word

    # عرض السؤال
    st.subheader(f"ما معنى كلمة: **{word['English Word']}**؟")

    # تجهيز خيارات الإجابة
    correct_ans = word['Arabic Translation']
    wrong_answers = df[df['Arabic Translation'] != correct_ans]['Arabic Translation'].sample(3).tolist()
    options = wrong_answers + [correct_ans]
    random.shuffle(options)

    # عرض أزرار الخيارات
    col1, col2 = st.columns(2)
    for i, option in enumerate(options):
        with col1 if i % 2 == 0 else col2:
            if st.button(option, key=option, use_container_width=True):
                if option == correct_ans:
                    st.success("أحسنت! إجابة صحيحة 🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"للأسف خطأ! الصحيح هو: {correct_ans}")
                
                st.session_state.count += 1
                # اختيار كلمة جديدة للسؤال القادم
                st.session_state.current_word = df.sample(1).iloc[0]
                st.rerun()

    st.divider()
    st.info(f"📊 نتيجتك الحالية: {st.session_state.score} من أصل {st.session_state.count}")

except Exception as e:
    st.warning("انتظر! تأكد من رفع ملف الكلمات باسم 'vocab.csv' في نفس الصفحة.")
  
