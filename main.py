import streamlit as st
import random
import time

# --- 1. التنسيق البصري الملكي (التصميم اللي تحبه) ---
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

# --- 2. القاموس (الوجبة الكبيرة من الكلمات مثبتة هنا) ---
if 'all_words' not in st.session_state:
    # قائمة طويلة جداً لضمان عدم ظهور "9 كلمات" فقط
    st.session_state.all_words = [
        {"en": "The", "ar": "ال"}, {"en": "Of", "ar": "من"}, {"en": "And", "ar": "و"},
        {"en": "A", "ar": "واحد"}, {"en": "To", "ar": "إلى"}, {"en": "In", "ar": "في"},
        {"en": "Is", "ar": "يكون"}, {"en": "You", "ar": "أنت"}, {"en": "That", "ar": "ذلك"},
        {"en": "It", "ar": "هو/هي"}, {"en": "He", "ar": "هو"}, {"en": "For", "ar": "لأجل"},
        {"en": "Was", "ar": "كان"}, {"en": "On", "ar": "على"}, {"en": "Are", "ar": "يكونون"},
        {"en": "As", "ar": "كما"}, {"en": "With", "ar": "مع"}, {"en": "His", "ar": "له"},
        {"en": "They", "ar": "هم"}, {"en": "I", "ar": "أنا"}, {"en": "At", "ar": "في"},
        {"en": "Be", "ar": "يكون"}, {"en": "This", "ar": "هذا"}, {"en": "Have", "ar": "يملك"},
        {"en": "From", "ar": "من"}, {"en": "Or", "ar": "أو"}, {"en": "One", "ar": "واحد"},
        {"en": "Had", "ar": "كان يملك"}, {"en": "By", "ar": "بواسطة"}, {"en": "Words", "ar": "كلمات"},
        {"en": "But", "ar": "لكن"}, {"en": "Not", "ar": "ليس"}, {"en": "What", "ar": "ماذا"},
        {"en": "All", "ar": "الكل"}, {"en": "Were", "ar": "كانوا"}, {"en": "We", "ar": "نحن"},
        {"en": "When", "ar": "عندما"}, {"en": "Your", "ar": "لك"}, {"en": "Can", "ar": "يستطيع"},
        {"en": "Said", "ar": "قال"}, {"en": "There", "ar": "هناك"}, {"en": "Use", "ar": "يستخدم"},
        {"en": "An", "ar": "واحد"}, {"en": "Each", "ar": "كل"}, {"en": "Which", "ar": "أي"},
        {"en": "She", "ar": "هي"}, {"en": "Do", "ar": "يفعل"}, {"en": "How", "ar": "كيف"},
        {"en": "Their", "ar": "لهم"}, {"en": "If", "ar": "إذا"}, {"en": "Will", "ar": "سوف"},
        {"en": "Up", "ar": "أعلى"}, {"en": "Other", "ar": "آخر"}, {"en": "About", "ar": "عن"},
        {"en": "Out", "ar": "خارج"}, {"en": "Many", "ar": "كثير"}, {"en": "Then", "ar": "ثم"},
        {"en": "Them", "ar": "هم"}, {"en": "These", "ar": "هذه"}, {"en": "So", "ar": "لذا"},
        {"en": "Some", "ar": "بعض"}, {"en": "Her", "ar": "لها"}, {"en": "Would", "ar": "سوف"},
        {"en": "Make", "ar": "يصنع"}, {"en": "Like", "ar": "مثل"}, {"en": "Him", "ar": "هو"},
        {"en": "Into", "ar": "داخل"}, {"en": "Time", "ar": "وقت"}, {"en": "Has", "ar": "يملك"},
        {"en": "Look", "ar": "ينظر"}, {"en": "Two", "ar": "اثنان"}, {"en": "More", "ar": "أكثر"},
        {"en": "Write", "ar": "يكتب"}, {"en": "Go", "ar": "يذهب"}, {"en": "See", "ar": "يرى"},
        {"en": "Number", "ar": "رقم"}, {"en": "No", "ar": "لا"}, {"en": "Way", "ar": "طريق"},
        {"en": "Could", "ar": "استطاع"}, {"en": "People", "ar": "ناس"}, {"en": "My", "ar": "لي"},
        {"en": "Than", "ar": "من"}, {"en": "First", "ar": "أول"}, {"en": "Water", "ar": "ماء"},
        {"en": "Been", "ar": "كان"}, {"en": "Called", "ar": "نادى"}, {"en": "Who", "ar": "من"},
        {"en": "Am", "ar": "أكون"}, {"en": "Its", "ar": "له/لها"}, {"en": "Now", "ar": "الآن"},
        {"en": "Find", "ar": "يجد"}, {"en": "Long", "ar": "طويل"}, {"en": "Down", "ar": "أسفل"},
        {"en": "Day", "ar": "يوم"}, {"en": "Did", "ar": "فعل"}, {"en": "Get", "ar": "يحصل"},
        {"en": "Come", "ar": "يأتي"}, {"en": "Made", "ar": "صنع"}, {"en": "May", "ar": "ربما"},
        {"en": "Part", "ar": "جزء"}, {"en": "Work", "ar": "عمل"}
        # ملاحظة: يمكنك الاستمرار بإضافة الكلمات هنا لتصل لـ 1000
    ]

if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.all_words)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1C40F;'>📍 القائمة الملكية</h2>", unsafe_allow_html=True)
    page = st.radio("اختر القسم:", ["🏠 صفحة الترحيب", "📖 القاموس الكامل", "🎯 اختبار التحدي", "🏆 قائمة المتصدرين"])
    st.divider()
    st.markdown(f"### 🏆 نقاطك: {st.session_state.score}")
    st.markdown(f'<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">🔗 إدارة التطبيق</a>', unsafe_allow_html=True)

# --- 4. محتوى الصفحات ---

if page == "🏠 صفحة الترحيب":
    st.markdown('<div class="royal-title">🌟 أهلاً بك في الأكاديمية 🌟</div>', unsafe_allow_html=True)
    st.info(f"✅ القاموس الآن يحتوي على {len(st.session_state.all_words)} كلمة حقيقية ومثبتة!")

elif page == "📖 القاموس الكامل":
    st.title("📖 القاموس (الوجبة الكبيرة)")
    # عرض الكلمات مع الصوت
    for i, item in enumerate(st.session_state.all_words, 1):
        c1, c2 = st.columns([4, 1])
        c1.markdown(f"**{i}. {item['en']}** = <span style='color:#2ECC71;'>{item['ar']}</span>", unsafe_allow_html=True)
        if c2.button("🔊", key=f"d_snd_{i}"):
            st.audio(f"https://dict.youdao.com/dictvoice?audio={item['en']}&type=2")

elif page == "🎯 اختبار التحدي":
    st.markdown('<div class="royal-title">🎯 اختبر ذكاءك</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current_word["en"]}</div></div>', unsafe_allow_html=True)
    
    user_input = st.text_input("👇 اكتب المعنى بالعربي هنا", key="test_in").strip()
    
    c1, c2 = st.columns(2)
    if c1.button("✅ تحقق"):
        if user_input == st.session_state.current_word['ar']:
            st.success("✅ كفو! إجابة صحيحة (+10)")
            st.session_state.score += 10
            time.sleep(1)
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()
        else:
            # التعديل المطلوب: يعطي الترجمة ويعبر
            st.error(f"❌ خطأ! الترجمة هي: {st.session_state.current_word['ar']}")
            st.info("جاري الانتقال للكلمة التالية...")
            time.sleep(2)
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()

    if c2.button("🔊 نطق"):
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
        
