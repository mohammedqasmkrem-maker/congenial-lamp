import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات والجمالية الملكية ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: rgba(10, 25, 20, 0.98); color: white; }
    .royal-card { background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    .stButton>button { background-color: #D4AC0D !important; color: black !important; font-weight: bold !important; border-radius: 10px !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة من ملفك الخاص ---
@st.cache_data
def load_full_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة كامل الملف
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Success", "Arabic": "نجاح"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_full_vocab()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 4. الغرف الملكية ---

# (1) غرفة الدعاء
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر"):
        st.session_state.page = "hall"; st.rerun()

# (2) القصر الرئيسي
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    st.write(f"<p style='text-align:center;'>المكتبة جاهزة: {len(st.session_state.db)} كلمة</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس والنطق (الكل)"): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار التحقق ✅"): st.session_state.page = "test"; st.rerun()
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
    with col2:
        if st.button("⏳ تحدي الـ 60 ثانية 🔥"): 
            st.session_state.start_time = time.time()
            st.session_state.blitz_word = random.choice(st.session_state.db)
            st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ تكوين الجمل"): st.session_state.page = "sentences"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()

# (3) تحدي الـ 60 ثانية (مع زر التحقق)
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب"): st.session_state.page = "hall"; st.rerun()
    rem = 60 - int(time.time() - st.session_state.start_time)
    
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("العودة للقصر", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<div class='royal-card'><h1 style='color:red;'>⏳ {rem} ثانية</h1></div>", unsafe_allow_html=True)
        word = st.session_state.blitz_word
        st.markdown(f"<h3>ترجم الكلمة التالية بسرعة: <b class='gold-text'>{word['English']}</b></h3>", unsafe_allow_html=True)
        
        ans = st.text_input("أدخل الترجمة العربية:", key="blitz_input")
        
        if st.button("تحقق من الكلمة ✅"):
            if ans.strip() == word['Arabic']:
                st.session_state.score += 50
                st.session_state.blitz_word = random.choice(st.session_state.db)
                st.success("صح! استمر...")
                time.sleep(0.5); st.rerun()
            else:
                st.error("خطأ! حاول مرة ثانية بسرعة")

# (4) القاموس (مربوط بالكامل بملفك)
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر"): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 مكتبة كلماتك الحقيقية</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن كلمة:")
    for i, w in enumerate(st.session_state.db[:200]): # عرض عينة للسرعة
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            c1, c2 = st.columns([5, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"sp_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['English']}&type=2")

# (5) الملف الشخصي الحقيقي
elif st.session_state.page == "profile":
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown(f"<div class='royal-card'><h1>👤 ملفك الشخصي</h1><h2>نقاطك الحالية: {st.session_state.score}</h2><h3>الرتبة: ملك الكلمات 👑</h3></div>", unsafe_allow_html=True)

# (6) تكوين الجمل
elif st.session_state.page == "sentences":
    if st.button("🔙 العودة"): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>ضع كلمة ({word['Arabic']}) في مكانها:</h3><h2>I like my __.</h2></div>", unsafe_allow_html=True)
    ans = st.text_input("اكتب الكلمة بالإنجليزية:")
    if st.button("تحقق ✅"):
        if ans.lower().strip() == word['English'].lower():
            st.success("بطل! جملة صحيحة"); st.session_state.score += 30; time.sleep(1); st.rerun()

# (7) غرفة الاسترخاء
elif st.session_state.page == "relax":
    if st.button("🔙"): st.session_state.page = "hall"; st.rerun()
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    
