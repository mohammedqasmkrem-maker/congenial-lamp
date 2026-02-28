import streamlit as st
import random

# --- 1. التنسيق البصري الملكي ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B1E26; color: white; }
    .royal-title { color: #F1C40F; font-size: 35px; font-weight: bold; text-align: center; }
    .word-frame { border: 3px solid #F1C40F; border-radius: 20px; padding: 20px; text-align: center; margin: 15px 0; }
    .en-word { color: #5DADE2; font-size: 40px; font-weight: bold; }
    .stButton>button {
        background-color: #F1C40F; color: black; border-radius: 20px; 
        font-weight: bold; width: 100%; border: none;
    }
    .sidebar-link {
        display: block; padding: 10px; background-color: #1C232D;
        color: #F1C40F !important; text-decoration: none;
        border-radius: 10px; border: 1px solid #F1C40F; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. بيانات المستويات ---
if 'score' not in st.session_state: st.session_state.score = 0
levels_data = {
    "المستوى 1 (أساسيات)": [
        {"en": "He", "ar": "هو", "hint": "للمذكر"},
        {"en": "She", "ar": "هي", "hint": "للمؤنث"},
        {"en": "You", "ar": "أنت", "hint": "للمخاطب"}
    ],
    "المستوى 2 (أفعال)": [
        {"en": "Tell", "ar": "يخبر", "hint": "يعطي معلومة"},
        {"en": "Go", "ar": "يذهب", "hint": "يتحرك لمكان"},
        {"en": "Eat", "ar": "يأكل", "hint": "يتناول الطعام"}
    ],
    "المستوى 3 (متقدم)": [
        {"en": "Success", "ar": "نجاح", "hint": "عكس الفشل"},
        {"en": "Future", "ar": "مستقبل", "hint": "الأيام القادمة"}
    ]
}

# دمج كل الكلمات للاختبار
all_words = [w for l in levels_data.values() for w in l]
if 'current' not in st.session_state: st.session_state.current = random.choice(all_words)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 ابدأ من هنا</h2>", unsafe_allow_html=True)
    page = st.radio("اختر الصفحة:", ["🏠 صفحة الترحيب", "📖 القاموس (مستويات)", "🎯 اختبار التحدي", "🏆 قائمة المتصدرين"])
    
    st.divider()
    st.markdown('<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق الخاص بك</a>', unsafe_allow_html=True)
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 مرحباً بك في <br> منزلك التعليمي الفخم 🌟</div>', unsafe_allow_html=True)
    st.write("---")
    st.info("👋 أهلاً بك! اختر القاموس لتعلم المستويات أو الاختبار لتحدي نفسك.")

elif page == "📖 القاموس (مستويات)":
    st.title("📖 القاموس المقسم")
    # اختيار المستوى داخل صفحة القاموس (نظام الصفحات)
    selected_level = st.selectbox("اختر المستوى التعليمي:", list(levels_data.keys()))
    
    st.markdown(f"### 📁 {selected_level}")
    for i, item in enumerate(levels_data[selected_level], 1):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {i}. {item['en']} = <span style='color:#2ECC71;'>{item['ar']}</span>", unsafe_allow_html=True)
        with c2:
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={item['en']}&tl=en&client=tw-ob"
            if st.button(f"🔊", key=f"voc_{selected_level}_{i}"):
                st.audio(tts_url)

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبر ذكاءك</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current["en"]}</div></div>', unsafe_allow_html=True)
    
    ans = st.text_input("👇 اكتب الحل بالعربي هنا").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تحقق"):
            if ans == st.session_state.current['ar']:
                st.success("أحسنت! +10 نقاط")
                st.session_state.score += 10
                st.session_state.current = random.choice(all_words)
                st.rerun()
            else:
                st.error("خطأ! تبقى نفس الكلمة")
    with col2:
        test_tts = f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.current['en']}&tl=en&client=tw-ob"
        if st.button("🔊 اسمع"):
             st.audio(test_tts)

elif page == "🏆 قائمة المتصدرين":
    st.title("🏆 لوحة الأبطال")
    st.write(f"**🥇 محمد البطل** : 1500 نقطة")
    st.write(f"**🥈 أنت** : {st.session_state.score} نقطة")
