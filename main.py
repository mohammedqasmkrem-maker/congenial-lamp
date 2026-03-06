import streamlit as st
import random
import time
import requests
import re

# --- 1. واجهة المستخدم الزجاجية الفاخرة ---
st.set_page_config(page_title="Abt Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000");
        background-size: cover; background-attachment: fixed;
    }
    .glass-box {
        background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 30px; color: white; text-align: center;
        max-width: 900px; margin: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1) !important; color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 18px !important; height: 65px !important; font-size: 20px !important;
        font-weight: bold !important; width: 100%; transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.3) !important; transform: scale(1.03);
        border: 1px solid #D4AC0D !important;
    }
    .word-item {
        background: rgba(255, 255, 255, 0.08); padding: 18px; border-radius: 20px;
        margin: 12px 0; border-right: 8px solid #D4AC0D; display: flex;
        justify-content: space-between; align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الجرد والبيانات (الـ 1011 كلمة) ---
@st.cache_data
def get_abt_vocab():
    url = "https://raw.githubusercontent.com/mohammedqasmkrem-maker/congenial-lamp/main/vocab.csv"
    data = []
    try:
        r = requests.get(url)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if " - " in line:
                    parts = line.split(" - ")
                    eng = re.sub(r'[^a-zA-Z\s]', '', parts[0]).strip()
                    ara = parts[1].strip()
                    if eng and ara:
                        lv = "🟢 سهل" if len(eng) <= 4 else "🟡 متوسط" if len(eng) <= 7 else "🔴 صعب"
                        data.append({"eng": eng, "ara": ara, "lv": lv})
        return data
    except: return [{"eng": "Mountain", "ara": "جبل", "lv": "🟢 سهل"}]

# --- 3. إدارة الجلسة والتقدم ---
if 'db' not in st.session_state: st.session_state.db = get_abt_vocab()
if 'page' not in st.session_state: st.session_state.page = "dua"
if 'score' not in st.session_state: st.session_state.score = 0
if 'learned' not in st.session_state: st.session_state.learned = set()
if 'favs' not in st.session_state: st.session_state.favs = []

def play_sound(txt):
    st.audio(f"https://dict.youdao.com/dictvoice?audio={txt}&type=2")

# --- 4. الغرف الـ 20 ---

# [الغرفة 1: الدعاء]
if st.session_state.page == "dua":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<h1>✨ فاتحة العلم</h1>", unsafe_allow_html=True)
    st.write("### اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علماً.")
    if st.button("دخول الأكاديمية (بسم الله)"):
        st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [الغرفة 2: القصر الرئيسي]
elif st.session_state.page == "hall":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown(f"<h1>🏔️ إمبراطورية أبت</h1>", unsafe_allow_html=True)
    
    # ميزة العداد الحقيقي (من أصل 1011)
    total_words = len(st.session_state.db)
    learned_count = len(st.session_state.learned)
    progress = (learned_count / total_words) * 100
    st.write(f"📊 تم جرد **{total_words}** كلمة بنجاح من ملفك")
    st.progress(progress / 100)
    st.write(f"أنجزت حفظ {learned_count} كلمة")

    if st.button("📖 القاموس الذكي (المستويات)"): st.session_state.page = "dict"; st.rerun()
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚔️ غرفة الاختبار"): 
            st.session_state.q = random.choice(st.session_state.db)
            st.session_state.page = "test"; st.rerun()
        if st.button("👤 الملف الشخصي"): st.session_state.page = "profile"; st.rerun()
    with c2:
        if st.button("⏳ تحدي الـ 60 ثانية"): st.session_state.page = "blitz"; st.rerun()
        if st.button("🌿 غرفة الاسترخاء"): st.session_state.page = "relax"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [الغرفة 3: القاموس]
elif st.session_state.page == "dict":
    st.markdown('<div class="glass-box" style="max-width:1100px;">', unsafe_allow_html=True)
    if st.button("🔙 عودة للقصر"): st.session_state.page = "hall"; st.rerun()
    
    lv_choice = st.radio("تصفية الصعوبة:", ["الكل", "🟢 سهل", "🟡 متوسط", "🔴 صعب"], horizontal=True)
    search = st.text_input("🔍 ابحث في الـ 1011 كلمة...")
    
    filtered = [w for w in st.session_state.db if (lv_choice == "الكل" or w['lv'] == lv_choice) and (search.lower() in w['eng'].lower() or search in w['ara'])]
    
    for i, w in enumerate(filtered[:40]):
        st.markdown(f'<div class="word-item"><div><b>{w["eng"]}</b><br><small>{w["lv"]}</small></div><b>{w["ara"]}</b></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        if col1.button(f"🔊 نطق الكلمة", key=f"v_{i}"):
            play_sound(w['eng']); st.session_state.learned.add(w['eng'])
        if col2.button(f"⭐ أضف للمفضلة", key=f"f_{i}"):
            if w not in st.session_state.favs: st.session_state.favs.append(w)
    st.markdown('</div>', unsafe_allow_html=True)

# [الغرفة 4: الاختبار - مصلح ومحدث]
elif st.session_state.page == "test":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    if st.button("🔙 إنهاء الاختبار"): st.session_state.page = "hall"; st.rerun()
    
    q = st.session_state.q
    st.markdown(f"### ما معنى كلمة: <h1 style='color:#D4AC0D;'>{q['eng']}</h1>", unsafe_allow_html=True)
    user_ans = st.text_input("الإجابة العربية:")
    if st.button("تحقق من الإجابة ✅"):
        if user_ans.strip() == q['ara']:
            st.success("إجابة إمبراطورية! +20 نقطة")
            st.session_state.score += 20
            st.session_state.q = random.choice(st.session_state.db)
            time.sleep(1); st.rerun()
        else:
            st.error(f"للأسف خطأ، المعنى هو: {q['ara']}")
    st.markdown('</div>', unsafe_allow_html=True)

# [الغرفة 5: الاسترخاء]
elif st.session_state.page == "relax":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("### 🍃 فيديو استراحة المحارب")
    st.video("https://www.youtube.com/watch?v=0wt-HbRw_pw")
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [الغرفة 6: الملف الشخصي]
elif st.session_state.page == "profile":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown("<h2>👤 رتبة الإمبراطور</h2>", unsafe_allow_html=True)
    st.write(f"### مجموع نقاطك: {st.session_state.score}")
    st.write(f"### كلمات أتقنت نطقها: {len(st.session_state.learned)}")
    if st.button("🔙 عودة"): st.session_state.page = "hall"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
                
