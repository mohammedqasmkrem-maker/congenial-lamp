import streamlit as st
import pandas as pd
import random
import os
import time
import streamlit.components.v1 as components

# 1. إعدادات المظهر والجمالية
st.set_page_config(page_title="واحة اللغة الملكية", layout="wide")

# وظيفة النطق + أصوات التفاعل + موسيقى الشلالات
def play_assets(text="", sound_type=None):
    # روابط أصوات (صح، خطأ، شلالات)
    success_sd = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
    fail_sd = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    nature_bg = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" # موسيقى هادئة تشبه الطبيعة
    
    sound_script = ""
    if sound_type == "success": sound_script = f'new Audio("{success_sd}").play();'
    elif sound_type == "fail": sound_script = f'new Audio("{fail_sd}").play();'
    
    components.html(f"""
        <script>
            // تشغيل موسيقى الخلفية (الشلالات) إذا لم تكن تعمل
            if (!window.bgAudio) {{
                window.bgAudio = new Audio("https://www.zapsplat.com/wp-content/uploads/2015/sound-effects-four/nature_waterfall_small_stream_close_up.mp3");
                window.bgAudio.loop = true;
                window.bgAudio.volume = 0.3;
                window.bgAudio.play();
            }}
            {sound_script}
            // نطق الكلمة الإنجليزية بصوت طبيعي
            if ("{text}" !== "") {{
                var msg = new SpeechSynthesisUtterance("{text}");
                msg.lang = "en-US";
                msg.rate = 0.8;
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """, height=0)

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: #f0f0f0; }
    h1 { color: #ffd700 !important; text-align: center; text-shadow: 2px 2px #000; font-size: 45px; }
    .stButton>button { 
        background-color: #ffd700; color: #000; border-radius: 30px; 
        font-weight: bold; border: none; height: 55px; transition: 0.4s;
    }
    .stButton>button:hover { background-color: #ffffff; transform: translateY(-3px); }
    .stTable { background-color: rgba(255, 255, 255, 0.1); border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. البيانات والمستويات
@st.cache_data
def load_data():
    if os.path.exists('vocab.csv'):
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    else:
        df = pd.DataFrame({'full_line': ["Dream - حلم", "Nature - طبيعة", "Waterfall - شلال"]})
    lvls = { (i//100)+1 : df['full_line'].iloc[i:i+100].values for i in range(0, len(df), 100) }
    return df, lvls

df_all, levels = load_data()

if 'score' not in st.session_state: st.session_state.score = 0
if 'lvl' not in st.session_state: st.session_state.lvl = 1

# 3. القائمة الجانبية
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>🌊 واحة الهدوء</h2>", unsafe_allow_html=True)
    page = st.radio("القائمة:", ["🏠 الرئيسية", "🎯 التحدي الهادئ", "📖 القاموس المبوب"])
    st.write("---")
    st.metric("نقاط الإنجاز 🏆", st.session_state.score)
    st.write(f"المستوى: {st.session_state.lvl}")
    st.info("الموسيقى تعمل تلقائياً في الخلفية 🔊")

# 4. التحدي (تبديل آلي + نطق + شلالات)
if page == "🎯 التحدي الهادئ":
    st.title(f"🎯 المستوى {st.session_state.lvl}")
    words = levels.get(st.session_state.lvl, levels[1])
    
    if 'word_now' not in st.session_state:
        st.session_state.word_now = random.choice(words)
        st.session_state.t_start = time.time()
        play_assets(st.session_state.word_now.split('-')[0].strip()) # نطق أول كلمة

    dt = max(0, 30 - int(time.time() - st.session_state.t_start))
    st.progress(dt / 30)
    
    eng, arb = st.session_state.word_now.split('-')[0].strip(), st.session_state.word_now.split('-')[1].strip()
    st.markdown(f"<div style='background:rgba(0,0,0,0.5); padding:30px; border-radius:20px; text-align:center; font-size:40px; border:1px solid gold;'>{eng}</div>", unsafe_allow_html=True)
    
    ans = st.text_input("اكتب الحل بالعربي واضغط Enter:", key=f"key_{st.session_state.score}").strip()
    
    if ans:
        if ans == arb:
            st.session_state.score += 20
            st.session_state.word_now = random.choice(words)
            st.session_state.t_start = time.time()
            play_assets(st.session_state.word_now.split('-')[0].strip(), "success")
            if st.session_state.score % 200 == 0: st.session_state.lvl += 1; st.balloons()
            st.rerun()
        else:
            play_assets("", "fail")
            st.error(f"❌ الجواب هو: {arb}")

# 5. القاموس (صفحات)
elif page == "📖 القاموس المبوب":
    st.title("📖 تصفح الكلمات الهادئ")
    p_size = 20
    total = max(1, len(df_all) // p_size)
    p_num = st.selectbox("الصفحة:", range(1, total + 1))
    st.table(df_all.iloc[(p_num-1)*p_size : p_num*p_size])
    
