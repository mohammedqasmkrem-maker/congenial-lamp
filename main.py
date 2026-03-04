import streamlit as st
import random
import time

# --- 1. التنسيق البصري (The Royal Oxford Style) ---
st.set_page_config(page_title="Abt Royal Academy", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0B1E26, #1C232D); color: #EAECEE; }
    .royal-title { color: #F1C40F; font-size: 40px; font-weight: bold; text-align: center; text-shadow: 2px 2px #000; }
    .word-frame { 
        border: 3px solid #D4AC0D; border-radius: 20px; padding: 40px; 
        text-align: center; margin: 20px 0; background: rgba(28, 35, 45, 0.9);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .en-word { color: #5DADE2; font-size: 60px; font-weight: bold; }
    .badge-gold { 
        background: linear-gradient(45deg, #D4AC0D, #F1C40F); 
        color: black; padding: 5px 15px; border-radius: 15px; 
        font-weight: bold; font-size: 14px; 
    }
    .stButton>button {
        background-color: #D4AC0D; color: black; border-radius: 25px; 
        font-weight: bold; width: 100%; height: 50px; border: none;
    }
    .sidebar-link {
        display: block; padding: 12px; background-color: #1C232D;
        color: #F1C40F !important; text-decoration: none;
        border-radius: 10px; border: 1px solid #D4AC0D; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاعدة بيانات الـ 1000 كلمة (الأكثر شيوعاً) ---
if 'all_words' not in st.session_state:
    # ملاحظة: هذه الوجبة الأولى، يمكنك لصق بقية الكلمات هنا بنفس التنسيق
    st.session_state.all_words = [
        {"en": "Ability", "ar": "قدرة"}, {"en": "Above", "ar": "فوق"}, {"en": "Accept", "ar": "يقبل"},
        {"en": "Accident", "ar": "حادث"}, {"en": "Achieve", "ar": "يحقق"}, {"en": "Across", "ar": "عبر"},
        {"en": "Act", "ar": "يمثل"}, {"en": "Active", "ar": "نشيط"}, {"en": "Actual", "ar": "فعلي"},
        {"en": "Add", "ar": "يضيف"}, {"en": "Address", "ar": "عنوان"}, {"en": "Admit", "ar": "يعترف"},
        {"en": "Adult", "ar": "بالغ"}, {"en": "Advice", "ar": "نصيحة"}, {"en": "Afford", "ar": "يتوفر له ثمن"},
        {"en": "Afraid", "ar": "خائف"}, {"en": "After", "ar": "بعد"}, {"en": "Against", "ar": "ضد"},
        {"en": "Age", "ar": "عمر"}, {"en": "Agree", "ar": "يوافق"}, {"en": "Ahead", "ar": "أمام"},
        {"en": "Allow", "ar": "يسمح"}, {"en": "Almost", "ar": "تقريباً"}, {"en": "Alone", "ar": "وحيد"},
        {"en": "Along", "ar": "على طول"}, {"en": "Already", "ar": "بالفعل"}, {"en": "Always", "ar": "دائماً"},
        {"en": "Amount", "ar": "كمية"}, {"en": "Ancient", "ar": "قديم"}, {"en": "Anger", "ar": "غضب"},
        {"en": "Animal", "ar": "حيوان"}, {"en": "Answer", "ar": "إجابة"}, {"en": "Anxious", "ar": "قلق"},
        {"en": "Appear", "ar": "يظهر"}, {"en": "Apply", "ar": "يقدم طلب"}, {"en": "Area", "ar": "منطقة"},
        {"en": "Argue", "ar": "يُجادل"}, {"en": "Arm", "ar": "ذراع"}, {"en": "Army", "ar": "جيش"},
        {"en": "Around", "ar": "حول"}, {"en": "Arrive", "ar": "يصل"}, {"en": "Art", "ar": "فن"},
        {"en": "Article", "ar": "مقال"}, {"en": "Aside", "ar": "جانباً"}, {"en": "Ask", "ar": "يسأل"},
        {"en": "Asleep", "ar": "نائم"}, {"en": "Assume", "ar": "يفترض"}, {"en": "Attack", "ar": "هجوم"},
        {"en": "Attend", "ar": "يحضر"}, {"en": "Attention", "ar": "انتباه"}, {"en": "Aunt", "ar": "عمة/خالة"},
        {"en": "Avoid", "ar": "يتجنب"}, {"en": "Award", "ar": "جائزة"}, {"en": "Aware", "ar": "مدرك"},
        {"en": "Away", "ar": "بعيداً"}, {"en": "Awful", "ar": "فظيع"}, {"en": "Baby", "ar": "طفل رضيع"},
        {"en": "Back", "ar": "خلف/ظهر"}, {"en": "Bad", "ar": "سيء"}, {"en": "Balance", "ar": "توازن"},
        {"en": "Ball", "ar": "كرة"}, {"en": "Bank", "ar": "بنك"}, {"en": "Bar", "ar": "قضيب"},
        {"en": "Base", "ar": "قاعدة"}, {"en": "Basic", "ar": "أساسي"}, {"en": "Basis", "ar": "أساس"},
        {"en": "Basket", "ar": "سلة"}, {"en": "Battle", "ar": "معركة"}, {"en": "Beach", "ar": "شاطئ"},
        {"en": "Bear", "ar": "دب/يتحمل"}, {"en": "Beat", "ar": "يهزم/يدق"}, {"en": "Beautiful", "ar": "جميل"},
        {"en": "Because", "ar": "لأن"}, {"en": "Become", "ar": "يصبح"}, {"en": "Bed", "ar": "سرير"},
        {"en": "Before", "ar": "قبل"}, {"en": "Begin", "ar": "يبدأ"}, {"en": "Behavior", "ar": "سلوك"},
        {"en": "Behind", "ar": "خلف"}, {"en": "Believe", "ar": "يعتقد/يؤمن"}, {"en": "Below", "ar": "أسفل"},
        {"en": "Benefit", "ar": "فائدة"}, {"en": "Beside", "ar": "بجانب"}, {"en": "Best", "ar": "الأفضل"},
        {"en": "Better", "ar": "أفضل"}, {"en": "Between", "ar": "بين"}, {"en": "Beyond", "ar": "ما وراء"},
        {"en": "Big", "ar": "كبير"}, {"en": "Bill", "ar": "فاتورة"}, {"en": "Birth", "ar": "ميلاد"},
        {"en": "Bit", "ar": "قليل"}, {"en": "Black", "ar": "أسود"}, {"en": "Blood", "ar": "دم"},
        {"en": "Blue", "ar": "أزرق"}, {"en": "Board", "ar": "لوحة"}, {"en": "Body", "ar": "جسم"},
        {"en": "Book", "ar": "كتاب"}, {"en": "Born", "ar": "مولود"}, {"en": "Both", "ar": "كلاهما"},
        {"en": "Bottom", "ar": "قاع"}, {"en": "Box", "ar": "صندوق"}, {"en": "Boy", "ar": "ولد"},
        # ... يمكنك إضافة بقية الـ 1000 هنا بنفس النمط
    ]

# --- 3. إدارة الحالة (State Management) ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.all_words)

def get_title(score):
    if score < 100: return "Beginner 🎖️"
    elif score < 300: return "Linguist 🎓"
    elif score < 600: return "Ambassador 🌍"
    else: return "King of English 👑"

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#F1C40F; text-align:center;'>Abt Royal App</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;'><span class='badge-gold'>{get_title(st.session_state.score)}</span></div>", unsafe_allow_html=True)
    st.write("---")
    page = st.radio("القائمة:", ["🏠 القاعة الرئيسية", "🎯 اختبار الذكاء", "📖 القاموس الملكي", "🏆 لوحة الأبطال"])
    st.divider()
    st.metric("مجموع نقاطك", st.session_state.score)
    st.markdown('<a href="https://share.streamlit.io/user/mqasmkrem-a11y" class="sidebar-link">⚙️ إدارة الأكاديمية</a>', unsafe_allow_html=True)

# --- 5. محتوى الصفحات ---

if page == "🏠 القاعة الرئيسية":
    st.markdown('<div class="royal-title">🌟 أهلاً بك في أكاديمية Abt 🌟</div>', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?q=80&w=1000&auto=format&fit=crop", caption="University of Oxford Style")
    st.info(f"تم تحميل {len(st.session_state.all_words)} كلمة حقيقية. هدفك اليوم هو الوصول للقب 'King'!")

elif page == "📖 القاموس الملكي":
    st.title("📖 القاموس الشامل")
    search = st.text_input("🔍 ابحث عن كلمة...")
    for item in st.session_state.all_words:
        if search.lower() in item['en'].lower() or search in item['ar']:
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{item['en']}** = {item['ar']}")
            if c2.button("🔊", key=f"snd_{item['en']}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={item['en']}&type=2")

elif page == "🎯 اختبار الذكاء":
    st.markdown('<div class="royal-title">🎯 التحدي الملكي</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="word-frame"><div class="en-word">{st.session_state.current_word["en"]}</div></div>', unsafe_allow_html=True)
    
    user_ans = st.text_input("اكتب الترجمة بالعربي وانقر 'تحقق'").strip()
    
    col1, col2 = st.columns(2)
    if col1.button("✅ تحقق من الإجابة"):
        if user_ans == st.session_state.current_word['ar']:
            st.success("✨ مذهل! إجابة صحيحة (+10)")
            st.session_state.score += 10
            time.sleep(1)
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()
        else:
            st.error(f"❌ خطأ! الترجمة الصحيحة هي: {st.session_state.current_word['ar']}")
            st.info("🔄 جاري الانتقال للكلمة التالية لتعزيز الحفظ...")
            time.sleep(2)
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()

    if col2.button("🔊 اسمع النطق"):
        st.audio(f"https://dict.youdao.com/dictvoice?audio={st.session_state.current_word['en']}&type=2")

elif page == "🏆 لوحة الأبطال":
    st.title("🏆 نخبة الدارسين")
    st.write(f"**🥇 محمد البطل** : 5000 نقطة")
    st.write(f"**🥈 أنت** : {st.session_state.score} نقطة")
    st.progress(min(st.session_state.score / 5000, 1.0))
        
