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
    .stMetric { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 15px; border: 1px solid gold; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة الصوت الذكية (شلالات + نطق)
def play_audio(text=""):
    components.html(f"""
        <script>
            // موسيقى الشلالات الهادئة
            if (!window.waterfall) {{
                window.waterfall = new Audio("https://www.zapsplat.com/wp-content/uploads/2015/sound-effects-four/nature_waterfall_small_stream_close_up.mp3");
                window.waterfall.loop = true;
                window.waterfall.volume = 0.2;
                window.waterfall.play();
            }}
            // نطق الكلمة الإنجليزية بصوت طبيعي
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
        df = pd.DataFrame({'full_line': ["Dream - حلم", "Success - نجاح", "World - عالم"]})
    lvls = { (i//100)+1 : df['full_line'].iloc[i:i+100].values for i in range(0, len(df), 100) }
    return df, lvls

df_all, levels = load_data()

if 'score' not in st.session_state: st.session_state.score = 0
if 'lvl' not in st.session_state: st.session_state.lvl = 1

# 4. القائمة الجانبية (بوابة النجوم)
with st.sidebar:
    st.markdown("## ⭐ بوابة النجوم ⭐")
    menu = st.radio("القائمة:", ["🏠 البيت الملكي", "🎯 تحدي النجوم", "📖 القاموس الناطق"])
    st.write("---")
    st.metric("رصيد النجوم ⭐", st.session_state.score // 20)
    st.write(f"المستوى الحالي: {st.session_state.lvl}")
    st.write("---")
    st.markdown(f"**🔗 رابط اللعبة العالمي:**")
    st.code("https://mohammedqasmkrem-maker.streamlit.app")

# 5. محتوى الصفحات
if menu == "🏠 البيت الملكي":
    st.markdown("<h1>🌟 مرحباً بك في منزلك التعليمي الفخم 🌟</h1>", unsafe_allow_html=True)
    st.write("##")
    st.markdown("### 🔊 لتفعيل الأجواء (شلالات + قراءة)، اضغط الزر:")
    if st.button("🌊 تشغيل الموسيقى والنجوم"):
        play_audio("Welcome to your academy")

elif menu == "🎯 تحدي النجوم":
    st.markdown(f"<h2>⭐ تحدي المستوى {st.session_state.lvl} ⭐</h2>", unsafe_allow_html=True)
    words = levels.get(st.session_state.lvl, levels[1])
    
    if 'game_word' not in st.session_state:
        st.session_state.game_word = random.choice(words)
        st.session_state.t0 = time.time()
        play_audio(st.session_state.game_word.split('-')[0].strip())

    dt = max(0, 30 - int(time.time() - st.session_state.t0))
    st.progress(dt / 30)
    
    eng, arb = st.session_state.game_word.split('-')[0].strip(), st.session_state.game_word.split('-')[1].strip()
    st.markdown(f"<div style='background:rgba(0,0,0,0.6); padding:40px; border-radius:25px; text-align:center; font-size:45px; border:3px solid gold;'>{eng}</div>", unsafe_allow_html=True)
    
    ans = st.text_input("اكتب الحل بالعربي هنا 👇", key=f"ans_{st.session_state.score}").strip()
    
    if ans:
        if ans == arb:
            st.success("⭐ أحسنت! كبل للكلمة التالية...")
            st.session_state.score += 20
            st.session_state.game_word = random.choice(words)
            st.session_state.t0 = time.time()
            play_audio(st.session_state.game_word.split('-')[0].strip())
            if st.session_state.score % 200 == 0: st.session_state.lvl += 1; st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ الجواب هو: {arb}")

elif menu == "📖 القاموس الناطق":
    st.markdown("<h1>📖 مكتبة الكلمات ⭐</h1>", unsafe_allow_html=True)
    p_size = 20
    total = max(1, len(df_all) // p_size)
    p_num = st.selectbox("اختر الصفحة:", range(1, total + 1))
    
    curr_page = df_all.iloc[(p_num-1)*p_size : p_num*p_size]
    for i, row in curr_page.iterrows():
        c1, c2 = st.columns([4, 1])
        with c1: st.write(f"### {row['full_line']}")
        with c2:
            if st.button("🔊", key=f"spk_{i}"):
                play_audio(row['full_line'].split('-')[0].strip())
    
