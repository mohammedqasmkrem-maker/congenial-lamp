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

# --- 2. محرك جلب الـ 1011 كلمة (بدون نقصان) ---
@st.cache_data
def load_all_words():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    try:
        # سحب الملف بالكامل وتجاهل الأخطاء البسيطة في التنسيق
        df = pd.read_csv(url, sep=' - ', engine='python', names=['English', 'Arabic'], on_bad_lines='skip')
        # تنظيف الأرقام (مثل "1. Time") من جهة الإنجليزي
        df['English'] = df['English'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
        df['Arabic'] = df['Arabic'].str.strip()
        return df.dropna().to_dict('records')
    except Exception as e:
        return [{"English": "Error", "Arabic": "فشل التحميل"}]

# --- 3. تهيئة النظام والذاكرة ---
if 'db' not in st.session_state: st.session_state.db = load_all_words()
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = "dua" # البداية الإجبارية هي الدعاء

# --- 4. نظام الغرف المنفصلة ---

# الغرفة (1): الدعاء (أول ما يفتح التطبيق)
if st.session_state.page == "dua":
    st.markdown("<div class='royal-card'><h1 class='gold-text'>✨ دعاء طلب العلم</h1><p style='font-size:26px;'>اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.</p></div>", unsafe_allow_html=True)
    if st.button("آمين - دخول الأكاديمية", use_container_width=True):
        st.session_state.page = "hall"
        st.rerun()

# الغرفة (2): القصر الرئيسي (التنقل)
elif st.session_state.page == "hall":
    st.markdown("<h1 style='text-align:center;' class='gold-text'>🌲 قصر Abt الملكي 🌲</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:white;'>عدد الكلمات المحملة: {len(st.session_state.db)} كلمة</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس والنطق 🔊", use_container_width=True): st.session_state.page = "dict"; st.rerun()
        if st.button("✍️ اختبار الكلمات (تحقق ✅)", use_container_width=True): st.session_state.page = "test"; st.rerun()
        if st.button("👤 الملف الشخصي الحقيقي", use_container_width=True): st.session_state.page = "profile"; st.rerun()
    with col2:
        if st.button("⏳ تحدي 60 ثانية (ذكاء)", use_container_width=True): 
            st.session_state.start_time = time.time(); st.session_state.page = "blitz"; st.rerun()
        if st.button("🛠️ بناء الجمل الملكي", use_container_width=True): st.session_state.page = "sentences"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء", use_container_width=True): st.session_state.page = "relax"; st.rerun()

# الغرفة (3): القاموس (بحث + نطق)
elif st.session_state.page == "dict":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.markdown("<h2 class='gold-text'>📖 مكتبة الـ 1011 كلمة</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن كلمة (إنجليزي أو عربي):")
    for i, w in enumerate(st.session_state.db[:200]): # عرض عينة كبيرة
        if search.lower() in w['English'].lower() or search in w['Arabic']:
            c1, c2 = st.columns([4, 1])
            c1.write(f"**{w['English']}** = {w['Arabic']}")
            if c2.button("🔊", key=f"voc_{i}"):
                st.audio(f"https://dict.youdao.com/dictvoice?audio={w['English']}&type=2")

# الغرفة (4): اختبار الكلمات مع زر التحقق
elif st.session_state.page == "test":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    if 'q_word' not in st.session_state: st.session_state.q_word = random.choice(st.session_state.db)
    word = st.session_state.q_word
    st.markdown(f"<div class='royal-card'><h2>{word['English']}</h2></div>", unsafe_allow_html=True)
    ans = st.text_input("ما الترجمة العربية؟")
    if st.button("تحقق من الإجابة ✅"):
        if ans.strip() == word['Arabic']:
            st.success("إجابة صحيحة! بطل")
            st.session_state.score += 10
            st.session_state.q_word = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"خطأ! الإجابة هي: {word['Arabic']}")

# الغرفة (5): تحدي الـ 60 ثانية (ذكاء اصطناعي)
elif st.session_state.page == "blitz":
    if st.button("🔙 انسحاب", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    elapsed = time.time() - st.session_state.start_time
    rem = 60 - int(elapsed)
    if rem <= 0:
        st.error("💥 انتهى الوقت!"); st.button("عودة", on_click=lambda: setattr(st.session_state, 'page', 'hall'))
    else:
        st.markdown(f"<h1 style='color:red; text-align:center;'>⏳ {rem} ثانية</h1>", unsafe_allow_html=True)
        word = random.choice(st.session_state.db)
        st.write(f"ترجم بسرعة: **{word['English']}**")
        if st.text_input("الإجابة:", key="bz").strip() == word['Arabic']:
            st.session_state.score += 60; st.rerun()

# الغرفة (6): غرفة الاسترخاء
elif st.session_state.page == "relax":
    if st.button("🔙 العودة للقصر", use_container_width=True): st.session_state.page = "hall"; st.rerun()
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    
