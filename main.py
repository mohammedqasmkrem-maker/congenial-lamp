import streamlit as st
import pandas as pd
import random
import time

# --- 1. الإعدادات البصرية والفخامة ---
st.set_page_config(page_title="Abt Royal Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000'); background-size: cover; background-attachment: fixed; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 25, 20, 0.98); z-index: -1; }
    .royal-card { background: rgba(25, 40, 35, 0.95); border: 2px solid #D4AC0D; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; color: white; }
    .gold-text { color: #D4AC0D !important; font-weight: bold; }
    </style>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب الـ 1011 كلمة بالكامل ---
@st.cache_data
def load_full_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # قراءة كل الكلمات بدون استثناء
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'])
        # تنظيف الأرقام والمسافات
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except:
        return [{"English": "Hello", "Arabic": "مرحباً"}]

# --- 3. تهيئة النظام ---
if 'db' not in st.session_state: st.session_state.db = load_full_vocab()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua"

# --- 4. غرف الأكاديمية المنظمة ---

# (1) غرفة الدعاء
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء البداية</h1><p style='font-size:24px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول القصر الملكي", use_container_width=True):
        st.session_state.page = "hall"; st.rerun()

# (2) القصر الملكي
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس والنطق 🔊", use_container_width=True): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار الكلمات (تحقق)", use_container_width=True): st.session_state.page = "test"; st.rerun()
    with col2:
        if st.button("⏳ تحدي 60 ثانية ⚡", use_container_width=True): 
            st.session_state.start_time = time.time(); st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ بناء الجمل", use_container_width=True): st.session_state.page = "sentences"; st.rerun()
    if st.button("👤 الملف الشخصي الحقيقي", use_container_width=True): st.session_state.page = "profile"; st.rerun()

# (3) القاموس مع النطق الصوتي
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 مكتبة الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن كلمة:")
    for i, w in enumerate(st.session_state.db[:100]): # عرض عينة للسرعة
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            c1, c2 = st.columns([4, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"sp_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['English']}&type=2")

# (4) اختبار الكلمات مع زر التحقق
elif st.session_state.page == "test":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    if 'curr' not in st.session_state: st.session_state.curr = random.choice(st.session_state.db)
    word = st.session_state.curr
    st.markdown(f"<div class='royal-card'><h2>{word['English']}</h2></div>", unsafe_allow_html=True)
    if st.button("اسمع الكلمة 🔊"): st.audio(f"https://dict.youdao.com/dictvoice?audio={word['English']}&type=2")
    ans = st.text_input("ما الترجمة العربية؟")
    if st.button("تحقق من الإجابة ✅"):
        if ans.strip() == word['Arabic']:
            st.success("إجابة صحيحة! بطل")
            st.session_state.score += 10; time.sleep(1); st.session_state.curr = random.choice(st.session_state.db); st.rerun()
        else:
            st.error(f"خطأ! الترجمة هي: {word['Arabic']}")

# (5) تحدي الـ 60 ثانية
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    rem = 60 - int(time.time() - st.session_state.start_time)
    if rem <= 0:
        st.error("انتهى الوقت!"); st.button("رجوع", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem}</h1>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("الإجابة:", key="bz").strip() == word['Arabic']:
            st.session_state.score += 60; st.rerun()

# (6) بناء الجمل
elif st.session_state.page == "sentences":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    word = random.choice(st.session_state.db)
    st.markdown(f"<div class='royal-card'><h3>I want to __ now.</h3><p>(المعنى: {word['Arabic']})</p></div>", unsafe_allow_html=True)
    if st.text_input("أكمل بالإنجليزية:").lower().strip() == word['English'].lower():
        st.success("بناء ملكي صحيح!"); st.session_state.score += 20; time.sleep(1); st.rerun()

# (7) الملف الشخصي
elif st.session_state.page == "profile":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.markdown(f"<div class='royal-card'><h1>👤 الملف الشخصي</h1><h2>إجمالي نقاطك: {st.session_state.score}</h2></div>", unsafe_allow_html=True)
    
