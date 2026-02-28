import streamlit as st
import random
import time
import sqlite3

# --- 1. إعدادات قاعدة البيانات (SQLite) لتخزين السكور والأسماء ---
def init_db():
    conn = sqlite3.connect('academy_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard 
                 (name TEXT, score INTEGER, level TEXT)''')
    conn.commit()
    conn.close()

def save_score(name, score, level):
    conn = sqlite3.connect('academy_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO leaderboard VALUES (?, ?, ?)", (name, score, level))
    conn.commit()
    conn.close()

init_db()

# --- 2. إعدادات الصفحة والوضع الليلي ---
st.set_page_config(page_title="أكاديمية مصباح لطيف", page_icon="💡")

# تنسيق الألوان والوضع الليلي (العربي أخضر / الإنجليزي أزرق)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; } /* وضع ليلي */
    .ar-text { color: #2ecc71; font-size: 28px; font-weight: bold; } /* أخضر */
    .en-text { color: #3498db; font-size: 28px; font-weight: bold; } /* أزرق */
    .stButton>button { border-radius: 20px; height: 3em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة (Session State) ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'player_name' not in st.session_state: st.session_state.player_name = ""
if 'level' not in st.session_state: st.session_state.level = 'Easy'
if 'repeat_used' not in st.session_state: st.session_state.repeat_used = False

# قاموس تجريبي (يمكنك توسيعه)
words_pool = {
    'Easy': [{'en': 'Apple', 'ar': 'تفاحة'}, {'en': 'Sun', 'ar': 'شمس'}],
    'Medium': [{'en': 'Knowledge', 'ar': 'معرفة'}, {'en': 'Success', 'ar': 'نجاح'}],
    'Hard': [{'en': 'Sustainability', 'ar': 'استدامة'}, {'en': 'Philosophy', 'ar': 'فلسفة'}]
}

# --- 4. صفحة الترحيب وتسجيل الاسم ---
if st.session_state.page == 'welcome':
    st.title("🌟 مرحباً بك في أكاديمية مصباح لطيف")
    name = st.text_input("سجل اسمك يا بطل:")
    level = st.selectbox("اختر مستوى التحدي:", ['Easy', 'Medium', 'Hard'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 القاموس"):
            if name:
                st.session_state.player_name = name
                st.session_state.level = level
                st.session_state.page = 'dictionary'
                st.rerun()
    with col2:
        if st.button("🎯 ابدأ الاختبار"):
            if name:
                st.session_state.player_name = name
                st.session_state.level = level
                st.session_state.page = 'quiz'
                st.session_state.current_word = random.choice(words_pool[level])
                st.rerun()

# --- 5. صفحة القاموس ---
elif st.session_state.page == 'dictionary':
    st.title(f"📖 قاموس - {st.session_state.level}")
    for item in words_pool[st.session_state.level]:
        st.markdown(f"<span class='en-text'>{item['en']}</span> : <span class='ar-text'>{item['ar']}</span>", unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'welcome'
        st.rerun()

# --- 6. صفحة الاختبار (المؤقت، النقاط، النطق) ---
elif st.session_state.page == 'quiz':
    st.header(f"🎯 المتسابق: {st.session_state.player_name}")
    st.subheader(f"المستوى: {st.session_state.level} | النقاط: {st.session_state.score}")
    
    # مؤقت تنازلي بسيط (مثلاً 30 ثانية)
    timer_placeholder = st.empty()
    
    st.markdown(f"ما معنى كلمة: <span class='en-text'>{st.session_state.current_word['en']}</span>", unsafe_allow_html=True)
    
    # ميزة النطق مرتين (وهمي عبر واجهة الصوت)
    if st.button("🔊 نطق الكلمة (مرتين)"):
        # ملاحظة: برمجياً نستخدم رابط صوتي مكرر
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.current_word['en']}&tl=en&total=2&idx=0&textlen=5&client=tw-ob")
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={st.session_state.current_word['en']}&tl=en&total=2&idx=1&textlen=5&client=tw-ob")

    ans = st.text_input("الإجابة بالعربي:", key="q_input")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("تحقق ✅"):
            if ans == st.session_state.current_word['ar']:
                st.success("أحسنت! +10")
                st.session_state.score += 10
                st.session_state.current_word = random.choice(words_pool[st.session_state.level])
                st.session_state.repeat_used = False
                st.rerun()
            else:
                st.error("❌ خطأ! تبقى نفس الكلمة.") # إذا يخطأ تبقى نفس الكلمة
    
    with col_b:
        if not st.session_state.repeat_used:
            if st.button("🔁 إعادة"):
                st.session_state.repeat_used = True
                st.info("لديك محاولة إعادة واحدة فقط لهذه الكلمة")
    
    with col_c:
        if st.button("🏁 إنهاء"):
            save_score(st.session_state.player_name, st.session_state.score, st.session_state.level)
            st.session_state.page = 'results'
            st.rerun()

# --- 7. صفحة النتائج و Leaderboard ---
elif st.session_state.page == 'results':
    st.title("📊 لوحة الشرف (Leaderboard)")
    st.balloons()
    st.success(f"عاشت إيدك يا {st.session_state.player_name}! نقاطك النهائية: {st.session_state.score}")
    
    # عرض الـ Leaderboard من القاعدة
    conn = sqlite3.connect('academy_data.db')
    import pandas as pd
    df = pd.read_sql_query("SELECT name, score, level FROM leaderboard ORDER BY score DESC LIMIT 5", conn)
    st.table(df)
    conn.close()
    
    if st.button("🔄 العودة للبداية (Reset)"):
        st.session_state.score = 0
        st.session_state.page = 'welcome'
        st.rerun()

# --- موسيقى خلفية هادئة ---
st.markdown("---")
st.write("🎵 موسيقى هادئة:")
st.audio("https://www.soundjay.com/nature/sounds/river-1.mp3")
st.markdown(f"[🔗 إدارة التطبيق](https://share.streamlit.io/user/mqasmkrem-a11y)")
