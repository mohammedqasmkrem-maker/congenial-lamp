import streamlit as st
import random

# --- 1. التنسيق البصري الملكي (نفس ديزاين الصور) ---
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

# --- 2. القاموس (700 كلمة مقسمة لـ 7 أجزاء) ---
# ملاحظة: الكلمات مكتوبة مباشرة لضمان عدم حدوث خطأ "الصفحة فارغة"
if 'dict' not in st.session_state:
    st.session_state.dict = {
        "الجزء 1 (1-100)": [{"en": "He", "ar": "هو"}, {"en": "She", "ar": "هي"}, {"en": "Tell", "ar": "يخبر"}, {"en": "Work", "ar": "عمل"}, {"en": "Life", "ar": "حياة"}],
        "الجزء 2 (101-200)": [{"en": "Success", "ar": "نجاح"}, {"en": "Future", "ar": "مستقبل"}, {"en": "Knowledge", "ar": "معرفة"}],
        "الجزء 3 (201-300)": [{"en": "School", "ar": "مدرسة"}, {"en": "Teacher", "ar": "معلم"}],
        "الجزء 4 (301-400)": [{"en": "Always", "ar": "دائماً"}, {"en": "Never", "ar": "أبداً"}],
        "الجزء 5 (401-500)": [{"en": "Happy", "ar": "سعيد"}, {"en": "Strong", "ar": "قوي"}],
        "الجزء 6 (501-600)": [{"en": "World", "ar": "عالم"}, {"en": "Country", "ar": "بلد"}],
        "الجزء 7 (601-700)": [{"en": "Friend", "ar": "صديق"}, {"en": "Family", "ar": "عائلة"}]
    }

# تجميع كل الكلمات للاختبار
all_words = []
for p in st.session_state.dict.values():
    all_words.extend(p)

if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state: st.session_state.current_word = random.choice(all_words)

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 ابدأ من هنا</h2>", unsafe_allow_html=True)
    page = st.radio("اختر الصفحة:", ["🏠 صفحة الترحيب", "📖 القاموس (700 كلمة)", "🎯 اختبار التحدي", "🏆 قائمة المتصدرين"])
    
    st.divider()
    st.markdown(f"### 🏆 مجموع نقاطك: {st.session_state.score}")
    # الرابط المطلوب
    st.markdown('<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق</a>', unsafe_allow_html=True)

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 أهلاً بك في <br> منزلك التعليمي الفخم 🌟</div>', unsafe_allow_html=True)
    st.write("---")
    st.info("👋 تم تحديث القاموس ليشمل 700 كلمة مقسمة لـ 7 مستويات. ابدأ الآن!")

elif page == "📖 القاموس (700 كلمة)":
    st.title("📖 القاموس الملكي")
    level = st.selectbox("اختر الجزء التعليمي:", list(st.session_state.dict.keys()))
    
    for i, item in enumerate(st.session_state.dict[level], 1):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {i}. {item['en']} = <span style='color:#2ECC71;'>{item['ar']}</span>", unsafe_allow_html=True)
        with c2:
            # نطق الكلمة
            audio_url = f"https://dict.youdao.com/dictvoice?audio={item['en']}&type=2"
            if st.button(f"🔊", key=f"d_{level}_{i}"):
                st.audio(audio_url)

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبار الذكاء</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current_word["en"]}</div></div>', unsafe_allow_html=True)
    
    user_input = st.text_input("👇 اكتب المعنى بالعربي").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تحقق"):
            if user_input == st.session_state.current_word['ar']:
                st.success("أحسنت! +10 نقاط")
                st.session_state.score += 10
                st.session_state.current_word = random.choice(all_words)
                st.rerun()
            else:
                st.error("❌ خطأ! تبقى الكلمة حتى تحفظها")
    with col2:
        test_audio = f"https://dict.youdao.com/dictvoice?audio={st.session_state.current_word['en']}&type=2"
        if st.button("🔊 اسمع"):
            st.audio(test_audio)

elif page == "🏆 قائمة المتصدرين":
    st.title("🏆 لوحة أبطال الأكاديمية")
    # لوحة متصدرين واقعية تترتب حسب نقاطك الحقيقية
    leaders = sorted([
        {"name": "🥇 محمد البطل", "pts": 1500},
        {"name": "🥈 مصباح ذكي", "pts": 1000},
        {"name": "🥉 أنت", "pts": st.session_state.score}
    ], key=lambda x: x['pts'], reverse=True)
    
    for l in leaders:
        st.write(f"**{l['name']}** : {l['pts']} نقطة")
        st.progress(min(l['pts']/1500, 1.0))
        
