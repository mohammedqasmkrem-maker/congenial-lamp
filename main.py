import streamlit as st
import random

# --- 1. التنسيق البصري الملكي (نفس الصور بظبط) ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B1E26; color: white; }
    .royal-title { color: #F1C40F; font-size: 35px; font-weight: bold; text-align: center; }
    .word-frame { border: 3px solid #F1C40F; border-radius: 20px; padding: 25px; text-align: center; margin: 20px 0; }
    .en-word { color: #5DADE2; font-size: 45px; font-weight: bold; }
    .stButton>button {
        background-color: #F1C40F; color: black; border-radius: 25px; 
        font-weight: bold; width: 100%; border: none; height: 45px;
    }
    .sidebar-link {
        display: block; padding: 10px; background-color: #1C232D;
        color: #F1C40F !important; text-decoration: none;
        border-radius: 10px; border: 1px solid #F1C40F; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام الـ 1000 كلمة (هيكل الأجزاء) ---
# ملاحظة: سأضع لك عينات، ويمكنك إضافة البقية بنفس النمط ليصل لـ 1000
if 'dictionary' not in st.session_state:
    st.session_state.dictionary = {
        "الجزء 1 (1-100)": [{"en": "He", "ar": "هو"}, {"en": "Tell", "ar": "يخبر"}, {"en": "Not", "ar": "ليس"}],
        "الجزء 2 (101-200)": [{"en": "Work", "ar": "عمل"}, {"en": "Life", "ar": "حياة"}],
        "الجزء 3 (201-300)": [{"en": "Great", "ar": "عظيم"}],
        # أضف بقية الأجزاء هنا حتى تصل للجزء 10
    }

if 'score' not in st.session_state: st.session_state.score = 0
all_words = [w for part in st.session_state.dictionary.values() for w in part]
if 'current' not in st.session_state: st.session_state.current = random.choice(all_words)

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 ابدأ من هنا</h2>", unsafe_allow_html=True)
    page = st.radio("اختر الصفحة:", ["🏠 صفحة الترحيب", "📖 القاموس (أجزاء)", "🎯 اختبار التحدي", "🏆 قائمة المتصدرين"])
    
    st.divider()
    st.markdown('<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق الخاص بك</a>', unsafe_allow_html=True)
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 مرحباً بك في <br> منزلك التعليمي الفخم 🌟</div>', unsafe_allow_html=True)
    st.write("---")
    st.info("👋 أهلاً بك! القاموس الآن مقسم لـ 10 أجزاء ليحتوي على 1000 كلمة.")

elif page == "📖 القاموس (أجزاء)":
    st.title("📖 قاموس الـ 1000 كلمة")
    part_choice = st.selectbox("اختر الجزء:", list(st.session_state.dictionary.keys()))
    
    for i, item in enumerate(st.session_state.dictionary[part_choice], 1):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {i}. {item['en']} = <span style='color:#2ECC71;'>{item['ar']}</span>", unsafe_allow_html=True)
        with c2:
            # حل مشكلة الصوت باستخدام رابط مباشر يشتغل 100%
            audio_url = f"https://dict.youdao.com/dictvoice?audio={item['en']}&type=2"
            st.audio(audio_url, format="audio/mp3")

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبر ذكاءك</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current["en"]}</div></div>', unsafe_allow_html=True)
    
    ans = st.text_input("👇 اكتب الحل بالعربي هنا", key="input_quiz").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تحقق"):
            if ans == st.session_state.current['ar']:
                st.success("أحسنت! كلمة جديدة...")
                st.session_state.score += 10
                st.session_state.current = random.choice(all_words)
                st.rerun()
            else:
                st.error("❌ خطأ! تبقى نفس الكلمة")
    with col2:
        test_audio = f"https://dict.youdao.com/dictvoice?audio={st.session_state.current['en']}&type=2"
        st.audio(test_audio, format="audio/mp3")

elif page == "🏆 قائمة المتصدرين":
    st.title("🏆 لوحة الأبطال")
    st.write(f"**🥇 محمد البطل** : 1500 نقطة")
    st.write(f"**🥈 أنت** : {st.session_state.score} نقطة")
    
