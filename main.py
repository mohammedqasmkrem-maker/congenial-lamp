import streamlit as st
import random

# --- 1. التنسيق البصري الملكي (نسخة طبق الأصل من صورك) ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B1E26; color: white; font-family: 'Cairo', sans-serif; }
    
    /* تصميم العنوان الكبير والأصفر */
    .royal-title { color: #F1C40F; font-size: 45px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    
    /* إطار الاختبار الذهبي */
    .word-frame { border: 3px solid #F1C40F; border-radius: 20px; padding: 25px; text-align: center; margin: 20px 0; }
    .en-word { color: #5DADE2; font-size: 40px; font-weight: bold; }
    
    /* الأزرار المدورة والصفراء */
    .stButton>button {
        background-color: #F1C40F; color: black; border-radius: 30px; 
        font-weight: bold; border: none; width: 100%; height: 50px;
    }
    
    /* القائمة الجانبية */
    [data-testid="stSidebar"] { background-color: #081419; border-right: 2px solid #F1C40F; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والنقاط الثابتة ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'words' not in st.session_state:
    st.session_state.words = [
        {"en": "He", "ar": "هو", "hint": "للمذكر"},
        {"en": "Tell", "ar": "يخبر", "hint": "يعطي معلومة"},
        {"en": "Success", "ar": "نجاح", "hint": "عكس الفشل"},
        {"en": "Light", "ar": "ضوء", "hint": "يأتي من المصباح"}
    ]
if 'current' not in st.session_state: st.session_state.current = random.choice(st.session_state.words)

# --- 3. القائمة الجانبية (Sidebar) مع السهم ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>🌟 القائمة الملكية</h2>", unsafe_allow_html=True)
    mode = st.radio("اختر القسم:", ["🎯 الاختبار الذكي", "📖 القاموس المستويات", "🏆 التنافس والمسابقات"])
    
    st.divider()
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")
    if st.button("🔄 ريست للكل"):
        st.session_state.score = 0
        st.rerun()

# --- 4. الأقسام (حسب اختيارك) ---

if mode == "🎯 الاختبار الذكي":
    st.markdown('<div class="royal-title">🌟 مرحباً بك في<br>منزلك التعليمي الفخم</div>', unsafe_allow_html=True)
    st.markdown(f"### 🏆 نقاطك الثابتة: {st.session_state.score}")
    
    # إطار الكلمة
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current["en"]}</div></div>', unsafe_allow_html=True)
    
    ans = st.text_input("👇 اكتب الحل بالعربي هنا", key="ans_box").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ خيار (تحقق)"):
            if ans == st.session_state.current['ar']:
                st.success("✨ أحسنت! كبل للكلمة التالية")
                st.session_state.score += 10
                st.session_state.current = random.choice(st.session_state.words)
                st.rerun()
            else:
                st.error("❌ خطأ! اضل بنفس الكلمة حتى تصحح") # شرطك: تضل بنفس الكلمة
    with col2:
        if st.button("🔊 نطق (مرتين)"):
            for _ in range(2):
                st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.current['en']}&tl=en&client=tw-ob")

    if st.button("💡 مساعدة"):
        st.info(f"تلميح للمساعدة: {st.session_state.current['hint']}")

elif mode == "📖 القاموس المستويات":
    st.title("📖 القاموس المرتب")
    for i, item in enumerate(st.session_state.words, 1):
        c1, c2 = st.columns([3, 1])
        with c1: st.markdown(f"### {i}. <span style='color:#F1C40F;'>{item['ar']}</span> - <span style='color:#5DADE2;'>{item['en']}</span>", unsafe_allow_html=True)
        with c2: 
            if st.button(f"🔊", key=f"snd_{i}"):
                st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={item['en']}&tl=en&client=tw-ob")

elif mode == "🏆 التنافس والمسابقات":
    st.title("⚔️ ساحة التنافس")
    st.markdown("### 🔥 المتصدرين حالياً (وهمي للتحفيز):")
    st.write("1. 🥇 محمد البطل - 1250 نقطة")
    st.write("2. 🥈 المستخدم المجهول - 1100 نقطة")
    st.write(f"3. 🥉 أنت - {st.session_state.score} نقطة")
    
    st.divider()
    st.markdown("### 🎮 مسابقة بين اثنين (قريباً)")
    st.info("هذا القسم قيد التطوير لتلعب ضد أصدقائك!")

# --- 5. الرابط في الأسفل ---
st.markdown("---")
st.markdown(f"[🔗 إدارة التطبيق](https://share.streamlit.io/user/mqasmkrem-a11y)")
    
