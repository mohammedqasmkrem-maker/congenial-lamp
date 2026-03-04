import streamlit as st
import random
import time

# --- 1. التصميم الملكي الثابت (الجبال والذهب) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(11, 30, 38, 0.92); z-index: -1;
    }
    .word-card {
        background: rgba(28, 35, 45, 0.95); border: 2px solid #D4AC0D;
        border-radius: 20px; padding: 60px; text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6); margin: 20px auto;
    }
    .gold-text { color: #D4AC0D !important; font-family: 'Georgia', serif; }
    .wax-seal {
        width: 90px; height: 90px; background: radial-gradient(#b3001b, #800012); 
        border-radius: 50%; border: 2px solid #D4AC0D; color: #D4AC0D; 
        line-height: 90px; text-align: center; font-weight: bold; 
        margin: 20px auto; box-shadow: 0 0 20px rgba(179, 0, 27, 0.8);
    }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. قاعدة بيانات الـ 100 كلمة الأولى (ترجمة عربية دقيقة) ---
if 'vocab' not in st.session_state:
    words_100 = [
        ("time", "وقت"), ("person", "شخص"), ("year", "سنة"), ("way", "طريق"), ("day", "يوم"),
        ("thing", "شيء"), ("man", "رجل"), ("world", "عالم"), ("life", "حياة"), ("hand", "يد"),
        ("part", "جزء"), ("child", "طفل"), ("eye", "عين"), ("woman", "امرأة"), ("place", "مكان"),
        ("work", "عمل"), ("week", "أسبوع"), ("case", "حالة"), ("point", "نقطة"), ("government", "حكومة"),
        ("company", "شركة"), ("number", "رقم"), ("group", "مجموعة"), ("problem", "مشكلة"), ("fact", "حقيقة"),
        ("be", "يكون"), ("have", "يملك"), ("do", "يفعل"), ("say", "يقول"), ("get", "يحصل"),
        ("make", "يصنع"), ("go", "يذهب"), ("know", "يعرف"), ("take", "يأخذ"), ("see", "يرى"),
        ("come", "يأتي"), ("think", "يفكر"), ("look", "ينظر"), ("want", "يريد"), ("give", "يعطي"),
        ("use", "يستخدم"), ("find", "يجد"), ("tell", "يخبر"), ("ask", "يسأل"), ("seem", "يبدو"),
        ("feel", "يشعر"), ("try", "يحاول"), ("leave", "يغادر"), ("call", "يتصل"), ("good", "جيد"),
        ("new", "جديد"), ("first", "أول"), ("last", "أخير"), ("long", "طويل"), ("great", "عظيم"),
        ("little", "صغير"), ("own", "يملك"), ("other", "آخر"), ("old", "قديم"), ("right", "حق/صحيح"),
        ("big", "كبير"), ("high", "عالٍ"), ("different", "مختلف"), ("small", "صغير"), ("large", "ضخم"),
        ("next", "التالي"), ("early", "مبكر"), ("young", "شاب"), ("important", "مهم"), ("few", "قليل"),
        ("public", "عام"), ("bad", "سيء"), ("same", "نفسه"), ("able", "قادر"), ("real", "حقيقي"),
        ("own", "خاص به"), ("just", "عادل/فقط"), ("best", "الأفضل"), ("better", "أفضل"), ("long", "طويل"),
        ("small", "صغير"), ("low", "منخفض"), ("early", "مبكر"), ("young", "شاب"), ("important", "مهم")
    ]
    st.session_state.vocab = [{"en": w[0], "ar": w[1]} for w in words_100]

if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state: st.session_state.current_word = random.choice(st.session_state.vocab)

# --- 3. الأقسام الملكية ---
with st.sidebar:
    st.markdown("<h1 class='gold-text'>👑 Abt Academy</h1>", unsafe_allow_html=True)
    menu = st.radio("القائمة:", ["🎯 التدريب", "📚 المكتبة (100 كلمة)", "🏆 المتصدرين"])
    st.metric("رصيد الهيبة", st.session_state.score)

# --- 4. المحتوى ---
if menu == "🎯 التدريب":
    st.markdown(f"<div class='word-card'><h1 class='gold-text' style='font-size:80px;'>{st.session_state.current_word['en']}</h1></div>", unsafe_allow_html=True)
    
    ans = st.text_input("أدخل الترجمة العربية...").strip()
    col1, col2 = st.columns(2)
    
    if col1.button("تحقق ✅"):
        if ans == st.session_state.current_word['ar']:
            st.session_state.score += 20
            st.markdown("<div class='wax-seal'>ABT</div>", unsafe_allow_html=True)
            st.success("إجابة ملكية! +20 نقطة")
            time.sleep(1)
            st.session_state.current_word = random.choice(st.session_state.vocab)
            st.rerun()
        else:
            st.error(f"الترجمة الصحيحة هي: {st.session_state.current_word['ar']}")
            time.sleep(2)
            st.rerun()

    if col2.button("🔊 نطق"):
        st.audio(f"https://dict.youdao.com/dictvoice?audio={st.session_state.current_word['en']}&type=2")

elif menu == "📚 المكتبة (100 كلمة)":
    st.markdown("<h2 class='gold-text'>المكتبة الملكية</h2>", unsafe_allow_html=True)
    for item in st.session_state.vocab:
        st.write(f"**{item['en']}** = {item['ar']}")

elif menu == "🏆 المتصدرين":
    st.markdown("<h2 class='gold-text'>لوحة المجد</h2>", unsafe_allow_html=True)
    st.write(f"1. محمد البطل - 5000 نقطة")
    st.write(f"2. أنت - {st.session_state.score} نقطة")
    
