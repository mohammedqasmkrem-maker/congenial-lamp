import streamlit as st
import random

# --- 1. الإعدادات والتنسيق الملكي ---
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

# --- 2. بيانات الـ 700 كلمة ---
if 'all_words' not in st.session_state:
    # عينة من الكلمات (يمكنك زيادتها لـ 700 بنفس النمط)
    st.session_state.all_words = [
        {"en": "He", "ar": "هو"}, {"en": "She", "ar": "هي"}, {"en": "Tell", "ar": "يخبر"},
        {"en": "Work", "ar": "عمل"}, {"en": "Success", "ar": "نجاح"}, {"en": "Future", "ar": "مستقبل"},
        {"en": "Life", "ar": "حياة"}, {"en": "Strong", "ar": "قوي"}, {"en": "Light", "ar": "ضوء"}
    ]

if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.all_words)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 ابدأ من هنا</h2>", unsafe_allow_html=True)
    page = st.radio("اختر الصفحة:", ["🏠 صفحة الترحيب", "📖 القاموس", "🎯 اختبار التحدي", "🏆 قائمة المتصدرين"])
    st.divider()
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")
    st.markdown(f'<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق</a>', unsafe_allow_html=True)

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 أهلاً بك في الأكاديمية 🌟</div>', unsafe_allow_html=True)
    st.info("تم إصلاح نظام الاختبار! الآن سيظهر لك إذا كان جوابك صح أو خطأ فوراً.")

elif page == "📖 القاموس":
    st.title("📖 القاموس التعليمي")
    for i, item in enumerate(st.session_state.all_words, 1):
        col1, col2 = st.columns([3, 1])
        col1.markdown(f"### {i}. {item['en']} = <span style='color:#2ECC71;'>{item['ar']}</span>", unsafe_allow_html=True)
        if col2.button("🔊", key=f"snd_{i}"):
            st.audio(f"https://dict.youdao.com/dictvoice?audio={item['en']}&type=2")

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبر ذكاءك</div>', unsafe_allow_html=True)
    
    # عرض الكلمة
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current_word["en"]}</div></div>', unsafe_allow_html=True)
    
    # حقل الإدخال
    user_answer = st.text_input("👇 اكتب المعنى بالعربي هنا", key="user_in").strip()
    
    c1, c2 = st.columns(2)
    
    # منطق التحقق المصلح
    if c1.button("✅ تحقق"):
        if user_answer == st.session_state.current_word['ar']:
            st.success("✅ أحسنت! إجابة صحيحة (+10 نقاط)")
            st.session_state.score += 10
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun() # تحديث الصفحة فوراً لتغيير الكلمة
        elif user_answer == "":
            st.warning("⚠️ الرجاء كتابة الإجابة أولاً")
        else:
            st.error(f"❌ خطأ! الإجابة ليست '{user_answer}'. حاول مجدداً")

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

