import streamlit as st
import random
import time

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

# --- 2. القاموس (الوجبة الأولى من الـ 700 كلمة) ---
if 'all_words' not in st.session_state:
    st.session_state.all_words = [
        {"en": "The", "ar": "ال"}, {"en": "Of", "ar": "من"}, {"en": "And", "ar": "و"},
        {"en": "A", "ar": "واحد"}, {"en": "To", "ar": "إلى"}, {"en": "In", "ar": "في"},
        {"en": "Is", "ar": "يكون"}, {"en": "You", "ar": "أنت"}, {"en": "That", "ar": "ذلك"},
        {"en": "It", "ar": "هو"}, {"en": "He", "ar": "هو"}, {"en": "For", "ar": "لأجل"},
        {"en": "Was", "ar": "كان"}, {"en": "On", "ar": "على"}, {"en": "Are", "ar": "يكونون"},
        {"en": "As", "ar": "كما"}, {"en": "With", "ar": "مع"}, {"en": "His", "ar": "له"},
        {"en": "They", "ar": "هم"}, {"en": "I", "ar": "أنا"}, {"en": "At", "ar": "في"},
        {"en": "Be", "ar": "يكون"}, {"en": "This", "ar": "هذا"}, {"en": "Have", "ar": "يملك"},
        {"en": "From", "ar": "من"}, {"en": "Or", "ar": "أو"}, {"en": "One", "ar": "واحد"},
        {"en": "Had", "ar": "كان يملك"}, {"en": "By", "ar": "بواسطة"}, {"en": "Words", "ar": "كلمات"},
        {"en": "But", "ar": "لكن"}, {"en": "Not", "ar": "ليس"}, {"en": "What", "ar": "ماذا"},
        {"en": "All", "ar": "الكل"}, {"en": "Were", "ar": "كانوا"}, {"en": "We", "ar": "نحن"},
        {"en": "When", "ar": "عندما"}, {"en": "Your", "ar": "لك"}, {"en": "Can", "ar": "يستطيع"},
        {"en": "Said", "ar": "قال"}, {"en": "There", "ar": "هناك"}, {"en": "Use", "ar": "يستخدم"}
    ]

if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.all_words)

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 القائمة</h2>", unsafe_allow_html=True)
    page = st.radio("اختر القسم:", ["🏠 صفحة الترحيب", "🎯 اختبار التحدي", "📖 القاموس الكامل", "🏆 قائمة المتصدرين"])
    st.divider()
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")
    st.markdown(f'<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق</a>', unsafe_allow_html=True)

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 أهلاً بك في الأكاديمية 🌟</div>', unsafe_allow_html=True)
    st.info("نظام الاختبار الجديد: إذا خطأت، يظهر لك الحل ويعبر للكلمة اللي بعدها!")

elif page == "📖 القاموس الكامل":
    st.title("📖 القاموس الكامل")
    for i, item in enumerate(st.session_state.all_words, 1):
        c1, c2 = st.columns([4, 1])
        c1.markdown(f"**{i}. {item['en']}** = {item['ar']}")
        if c2.button("🔊", key=f"d_{i}"):
            st.audio(f"https://dict.youdao.com/dictvoice?audio={item['en']}&type=2")

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبر ذكاءك</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current_word["en"]}</div></div>', unsafe_allow_html=True)
    
    # حقل الإدخال
    user_input = st.text_input("👇 اكتب المعنى بالعربي هنا", key="quiz_input").strip()
    
    c1, c2 = st.columns(2)
    
    if c1.button("✅ تحقق"):
        if user_input == st.session_state.current_word['ar']:
            st.success("✅ كفو! إجابة صحيحة (+10 نقاط)")
            st.session_state.score += 10
            time.sleep(1) # تأخير بسيط ليرى النتيجة
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()
        else:
            # هنا التعديل المطلوب: يظهر الخطأ والترجمة ثم ينتقل
            st.error(f"❌ خطأ! الترجمة الصحيحة هي: {st.session_state.current_word['ar']}")
            st.info("جاري الانتقال للكلمة التالية...")
            time.sleep(2) # يعطيه وقت يقرأ الترجمة الصحيحة
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()

    if c2.button("🔊 اسمع"):
        st.audio(f"https://dict.youdao.com/dictvoice?audio={st.session_state.current_word['en']}&type=2")

elif page == "🏆 قائمة المتصدرين":
    st.title("🏆 لوحة الأبطال")
    leaders = sorted([
        {"name": "🥇 محمد البطل", "pts": 1500},
        {"name": "🥈 مصباح ذكي", "pts": 1000},
        {"name": "🥉 أنت", "pts": st.session_state.score}
    ], key=lambda x: x['pts'], reverse=True)
    for l in leaders:
        st.write(f"**{l['name']}** : {l['pts']} نقطة")
        
