import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية (الغابة والجبال) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000');
        background-size: cover; background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(10, 25, 20, 0.97); z-index: -1;
    }
    .royal-card {
        background: rgba(20, 35, 30, 0.95); border: 2px solid #D4AC0D;
        border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. جلب الكلمات من ملف vocab.csv (سطر 12-14) ---
@st.cache_data
def load_vocab():
    # الرابط المباشر لملفك على GitHub المستخرج من الصورة
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة الملف وتنظيف الكلمات من الأرقام (مثل 1. Time)
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True)
        return df.to_dict('records')
    except:
        return [{"English": "Time", "Arabic": "الوقت"}]

# --- 3. تهيئة النظام (منع خطأ AttributeError) ---
if 'db' not in st.session_state:
    st.session_state.db = load_vocab()
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.page = "hall"
    st.session_state.current_word = random.choice(st.session_state.db)
    st.session_state.show_dua = True

# --- 4. نافذة الدعاء التلقائية ---
if st.session_state.show_dua:
    st.markdown("""<div style='background:#0a1a10; padding:30px; border:2px solid #D4AC0D; border-radius:15px; text-align:center;'>
    <h2 class='gold-text'>✨ دعاء طلب العلم</h2>
    <p style='color:white; font-size:22px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("آمين - دخول الأكاديمية", use_container_width=True):
        st.session_state.show_dua = False
        st.rerun()

# --- 5. الواجهة الرئيسية ---
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='royal-card'><h2 class='gold-text'>👤 الملف الشخصي</h2><p>نقاطك الحقيقية: {st.session_state.score} | الـ Streak: {st.session_state.streak}</p></div>", unsafe_allow_html=True)
        if st.button("فتح السجل 🎖️", use_container_width=True): st.session_state.page = "profile"

    with col2:
        st.markdown("<div class='royal-card'><h2 class='gold-text'>✍️ تحدي الكلمات</h2><p>اختبر كلماتك من ملف vocab.csv</p></div>", unsafe_allow_html=True)
        if st.button("بدء التحدي ⚔️", use_container_width=True): st.session_state.page = "game"

    st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 الطبيعة الحلال</h2><p>فيديو الاسترخاء والتركيز</p></div>", unsafe_allow_html=True)
    if st.button("دخول الغرفة 🧘", use_container_width=True): st.session_state.page = "nature"

    st.markdown(f"<p style='text-align:center; color:white;'>المنصة الرسمية: <a href='https://share.streamlit.io/user/mqasmkrem-a11y' style='color:#D4AC0D;'>mqasmkrem-a11y</a></p>", unsafe_allow_html=True)

# --- 6. منطق الغرف ---
elif st.session_state.page == "game":
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    word = st.session_state.current_word
    st.markdown(f"<div class='royal-card'><h1 class='gold-text'>{word['English']}</h1><p>ما ترجمة هذه الكلمة من ملفك؟</p></div>", unsafe_allow_html=True)
    
    ans = st.text_input("اكتب الترجمة العربية:").strip()
    if st.button("تحقق ✅"):
        if ans == word['Arabic']:
            st.session_state.score += 50
            st.session_state.streak += 1
            st.success("أحسنت! إجابة ملكية.")
            st.session_state.current_word = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"خطأ! الترجمة هي: {word['Arabic']}")
            st.session_state.streak = 0

elif st.session_state.page == "nature":
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text' style='text-align:center;'>🌿 غرفة الهدوء الملكية</h2>", unsafe_allow_html=True)
    # إضافة الفيديو المطلوب
    st.video("https://youtu.be/0wt-HbRw_pw?si=IJ23Q_Mcbb07Kdny")
                
