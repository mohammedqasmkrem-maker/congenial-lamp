import streamlit as st
import pandas as pd
import random
import os
import time
import streamlit.components.v1 as components

# 1. إعدادات المظهر والنجوم ⭐
st.set_page_config(page_title="أكاديمية النجوم الملكية", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: gold; }
    h1, h2, h3 { color: #ffd700 !important; text-align: center; text-shadow: 2px 2px #000; }
    .stButton>button { 
        background-color: #ffd700; color: #000; border-radius: 50px; 
        font-weight: bold; border: 3px solid #fff; height: 60px; font-size: 20px;
    }
    .stMetric { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة الصوت (الموسيقى + النطق) - تعمل بمجرد التفاعل
def play_all(text=""):
    components.html(f"""
        <script>
            // موسيقى الشلالات
            if (!window.bgMusic) {{
                window.bgMusic = new Audio("https://www.zapsplat.com/wp-content/uploads/2015/sound-effects-four/nature_waterfall_small_stream_close_up.mp3");
                window.bgMusic.loop = true;
                window.bgMusic.volume = 0.2;
                window.bgMusic.play();
            }}
            // نطق الكلمة
            if ("{text}" !== "") {{
                var msg = new SpeechSynthesisUtterance("{text}");
                msg.lang = "en-US";
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """, height=0)

# 3. تحميل البيانات والمستويات
@st.cache_data
def load_data():
    if os.path.exists('vocab.csv'):
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    else:
        df = pd.DataFrame({'full_line': [f"Star {i} - نجمة {i}" for i in range(1, 1001)]})
    lvls = { (i//100)+1 : df['full_line'].iloc[i:i+100].values for i in range(0, len(df), 100) }
    return df, lvls

df_all, levels = load_data()

if 'score' not in st.session_state: st.session_state.score = 0
if 'lvl' not in st.session_state: st.session_state.lvl = 1

# 4. القائمة الجانبية
with st.sidebar:
    st.markdown("## ⭐ لوحة الأبطال")
    menu = st.radio("القائمة الرئيسية:", ["🏠 شاشة البدء", "🎯 تحدي النجوم", "📖 قاموس الصفحات"])
    st.write("---")
    st.metric("رصيدك من النجوم ⭐", st.session_state.score // 20)
    st.write(f"المستوى الحالي: {st.session_state.lvl}")
    st.markdown("---")
    # رابط النشر الحقيقي
    st.markdown(f"**🔗 رابط المشاركة كبل:**")
    st.code("https://mohammedqasmkrem-maker.streamlit.app")

# 5. محتوى الصفحات
if menu == "🏠 شاشة البدء":
    st.markdown("<h1>🌟 مرحباً بك في أكاديمية النجوم 🌟</h1>", unsafe_allow_html=True)
    st.write("##")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 هل أنت مستعد للاختبار؟")
        if st.button("🚀 اذهب إلى التحدي الآن"):
            st.info("اضغط على 'تحدي النجوم' من القائمة الجانبية")
    with col2:
        st.markdown("### 📖 تصفح الكلمات")
        if st.button("📚 افتح القاموس المبوب"):
            st.info("اضغط على 'قاموس الصفحات' من القائمة الجانبية")
    st.write("---")
    st.markdown("<p style='text-align:center;'>ملاحظة: إذا لم تسمع الصوت، اضغط على أي زر في الشاشة لتفعيل الموسيقى.</p>", unsafe_allow_html=True)

elif menu == "🎯 تحدي النجوم":
    st.markdown(f"<h1>⭐ تحدي المستوى {st.session_state.lvl} ⭐</h1>", unsafe_allow_html=True)
    words = levels.get(st.session_state.lvl, levels[1])
    
    if 'current_word' not in st.session_state:
        st.session_state.current_word = random.choice(words)
        st.session_state.t_start = time.time()
        play_all(st.session_state.current_word.split('-')[0].strip())

    dt = max(0, 30 - int(time.time() - st.session_state.t_start))
    st.progress(dt / 30)
    
    eng, arb = st.session_state.current_word.split('-')[0].strip(), st.session_state.current_word.split('-')[1].strip()
    st.markdown(f"<div style='background:rgba(0,0,0,0.6); padding:40px; border-radius:25px; text-align:center; font-size:45px; border:3px solid gold;'>{eng}</div>", unsafe_allow_html=True)
    
    ans = st.text_input("أدخل الترجمة العربية هنا 👇", key=f"ans_{st.session_state.score}").strip()
    
    if ans:
        if ans == arb:
            st.success("⭐ أحسنت! إجابة صحيحة")
            st.session_state.score += 20
            st.session_state.current_word = random.choice(words)
            st.session_state.t_start = time.time()
            play_all(st.session_state.current_word.split('-')[0].strip()) # نطق الكلمة الجديدة
            if st.session_state.score % 200 == 0: 
                st.session_state.lvl += 1
                st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ خطأ! الجواب الصحيح: {arb}")

elif menu == "📖 قاموس الصفحات":
    st.markdown("<h1>📖 مكتبة الكلمات ⭐</h1>", unsafe_allow_html=True)
    p_size = 20
    total = max(1, len(df_all) // p_size)
    p_num = st.selectbox("اختر رقم الصفحة لتصفح الكلمات:", range(1, total + 1))
    st.table(df_all.iloc[(p_num-1)*p_size : p_num*p_size])
    
