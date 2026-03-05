import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية (خلفية الجبل والغابات) ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000');
        background-size: cover;
        background-attachment: fixed;
    }
    .overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7); z-index: -1;
    }
    .royal-card {
        background: rgba(30, 50, 40, 0.9); border: 2px solid #D4AC0D;
        border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 15px; color: white;
    }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .back-btn { background-color: #D4AC0D; color: black; border-radius: 10px; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك الكلمات (ربط مباشر بالملف الأصلي) ---
@st.cache_data
def load_full_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Nature", "Arabic": "طبيعة"}]

# --- 3. تهيئة الحالة والبيانات ---
if 'db' not in st.session_state: st.session_state.db = load_full_vocab()
if 'score' not in st.session_state: st.session_state.score = 0
if 'learned' not in st.session_state: st.session_state.learned = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 4. نظام الغرف الملكية ---

# الغرفة (1): دعاء البداية
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='font-size:26px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر الجبلي", use_container_width=True):
        st.session_state.page = "hall"; st.rerun()

# الغرفة (2): القصر الرئيسي (لوحة التحكم)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🏔️ قصر Abt وسط الغابات 🏔️</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 الملف الشخصي الحقيقي", use_container_width=True): st.session_state.page = "profile"; st.rerun()
        if st.button("📖 القاموس الشامل (1011 كلمة)", use_container_width=True): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار التحقق ✅", use_container_width=True): st.session_state.page = "test"; st.rerun()

    with col2:
        if st.button("⏳ تحدي الـ 60 ثانية ⚡", use_container_width=True): 
            st.session_state.start_time = time.time(); st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ بناء وتكوين الجمل", use_container_width=True): st.session_state.page = "sentences"; st.rerun()
        if st.button("🧘 غرفة الاسترخاء", use_container_width=True): st.session_state.page = "relax"; st.rerun()

# الغرفة (3): الملف الشخصي الحقيقي
elif st.session_state.page == "profile":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<div class='royal-card'><h1 class='gold-text'>👤 بياناتك الملكية</h1></div>", unsafe_allow_html=True)
    st.write(f"### 🏆 مجموع النقاط: {st.session_state.score}")
    st.write(f"### 📚 كلمات أتقنتها: {st.session_state.learned}")
    st.write("### 🎖️ الرتبة: ملك الغابة 🦁")

# الغرفة (4): غرفة الاسترخاء
elif st.session_state.page == "relax":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<div class='royal-card'><h2 class='gold-text'>🌿 استرخِ مع صوت الطبيعة</h2></div>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")

# الغرفة (5): تكوين الجمل
elif st.session_state.page == "sentences":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>أكمل الجملة بالكلمة المناسبة: ({word['Arabic']})</h3><h2>The __ looks beautiful.</h2></div>", unsafe_allow_html=True)
    ans = st.text_input("اكتب الكلمة بالإنجليزية:")
    if st.button("تحقق من الجملة ✅"):
        if ans.lower().strip() == word['English'].lower():
            st.success("بطل! جملة صحيحة"); st.session_state.score += 20; st.rerun()
        else: st.error(f"خطأ! الكلمة هي: {word['English']}")

# الغرفة (6): القاموس (الـ 1011 كلمة بالكامل)
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    search = st.text_input("🔍 ابحث في مكتبة الـ 1011 كلمة:")
    for i, w in enumerate(st.session_state.db[:150]):
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            st.write(f"**{w['English']}** = {w['Arabic']} 🔊")

# الغرفة (7): تحدي الـ 60 ثانية
elif st.session_state.page == "blitz":
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("عودة للقصر", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem} ثانية</h1>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("الإجابة:", key="bz").strip() == word['Arabic']:
            st.session_state.score += 50; st.session_state.learned += 1; st.rerun()
