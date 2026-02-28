import streamlit as st
import random

# --- 1. التنسيق البصري الملكي (نفس الصور) ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B1E26; color: white; }
    .royal-title { color: #F1C40F; font-size: 40px; font-weight: bold; text-align: center; }
    .word-frame { border: 3px solid #F1C40F; border-radius: 20px; padding: 25px; text-align: center; margin: 20px 0; }
    .en-word { color: #5DADE2; font-size: 45px; font-weight: bold; }
    .stButton>button {
        background-color: #F1C40F; color: black; border-radius: 25px; 
        font-weight: bold; width: 100%; border: none;
    }
    /* تنسيق الرابط في القائمة الجانبية */
    .sidebar-link {
        display: block; padding: 10px; background-color: #1C232D;
        color: #F1C40F !important; text-decoration: none;
        border-radius: 10px; border: 1px solid #F1C40F; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والنقاط ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'words' not in st.session_state:
    st.session_state.words = [
        {"en": "He", "ar": "هو", "hint": "للمذكر"},
        {"en": "Tell", "ar": "يخبر", "hint": "يعطي معلومة"},
        {"en": "Not", "ar": "ليس", "hint": "للنفي"},
        {"en": "As", "ar": "كما", "hint": "للتشبيه"},
        {"en": "You", "ar": "أنت", "hint": "للمخاطب"}
    ]
if 'current' not in st.session_state: st.session_state.current = random.choice(st.session_state.words)

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 ابدأ من هنا</h2>", unsafe_allow_html=True)
    page = st.radio("اختر الصفحة:", ["🏠 صفحة الترحيب", "📖 القاموس (مستويات)", "🎯 اختبار التحدي", "🏆 قائمة المتصدرين"])
    
    st.divider()
    # إضافة الرابط المطلوب في القائمة الجانبية
    st.markdown("### 🛠️ إعدادات الإدارة")
    st.markdown('<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق الخاص بك</a>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 مرحباً بك في <br> منزلك التعليمي الفخم 🌟</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.write("### 👋 أهلاً بك يا بطل!")
    st.info("استخدم القائمة الجانبية للانتقال بين الأقسام. ابدأ بالقاموس ثم الاختبار!")

elif page == "📖 القاموس (مستويات)":
    st.title("📖 قاموس المستويات")
    for i, item in enumerate(st.session_state.words, 1):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {i}. {item['en']} = <span style='color:#2ECC71;'>{item['ar']}</span>", unsafe_allow_html=True)
        with c2:
            # نطق الكلمة (تم التأكد من عمله)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={item['en']}&tl=en&client=tw-ob"
            if st.button(f"🔊", key=f"dict_{i}"):
                st.audio(tts_url)

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبر ذكاءك</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current["en"]}</div></div>', unsafe_allow_html=True)
    
    ans = st.text_input("👇 اكتب الحل بالعربي هنا").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تحقق"):
            if ans == st.session_state.current['ar']:
                st.success("أحسنت! كلمة جديدة...")
                st.session_state.score += 10
                st.session_state.current = random.choice(st.session_state.words)
                st.rerun() # لتغيير الكلمة فوراً
            else:
                st.error("خطأ! حاول مرة أخرى")
    with col2:
        test_tts = f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.current['en']}&tl=en&client=tw-ob"
        if st.button("🔊 اسمع"):
             st.audio(test_tts)

elif page == "🏆 قائمة المتصدرين":
    st.title("🏆 لوحة الأبطال")
    leaders = [
        {"name": "🥇 محمد البطل", "pts": 1500},
        {"name": "🥈 مصباح ذكي", "pts": 1200},
        {"name": "🥉 أنت", "pts": st.session_state.score}
    ]
    for l in leaders:
        st.write(f"**{l['name']}** : {l['pts']} نقطة")
    
