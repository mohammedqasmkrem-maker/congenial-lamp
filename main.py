import streamlit as st
import pandas as pd
import random
import os
import time
import urllib.parse

# 1. إعدادات الصفحة والتصميم الفخم (CSS)
st.set_page_config(page_title="أكاديمية اللغة الملكية", layout="wide")

st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    /* تنسيق العناوين */
    h1, h2, h3 {
        color: #e94560 !important;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    /* تنسيق الأزرار المركزية */
    div.stButton > button {
        background-color: #e94560;
        color: white;
        border-radius: 15px;
        height: 80px;
        font-size: 22px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0f3460;
        transform: scale(1.05);
        border: 1px solid #e94560;
    }
    /* القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #1a1a2e;
        border-right: 1px solid #e94560;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات والمستويات
@st.cache_data
def load_data():
    if os.path.exists('vocab.csv'):
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    else:
        df = pd.DataFrame({'full_line': [f"Word {i} - كلمة {i}" for i in range(1, 1001)]})
    
    # تقسيم الكلمات لمستويات (100 لكل مستوى)
    levels = { (i // 100) + 1 : df['full_line'].iloc[i:i+100].values for i in range(0, len(df), 100) }
    return df, levels

df_all, levels_dict = load_data()

# إدارة الحالة
if 'score' not in st.session_state: st.session_state.score = 0
if 'lvl' not in st.session_state: st.session_state.lvl = 1
if 'prizes' not in st.session_state: st.session_state.prizes = []

# --- 3. القائمة الجانبية الفخمة ---
with st.sidebar:
    st.markdown("<h2 style='color: #e94560;'>💎 الأكاديمية</h2>", unsafe_allow_html=True)
    menu = st.radio("القائمة:", ["🏠 الشاشة الرئيسية", "🎮 ابدأ التحدي", "📖 القاموس الملكي", "🏆 الجوائز"])
    st.write("---")
    st.metric("رصيد النقاط", st.session_state.score)
    st.write(f"المستوى الحالي: {st.session_state.lvl}")

# --- 4. محتوى الصفحات ---

if menu == "🏠 الشاشة الرئيسية":
    st.markdown("<h1>👋 أهلاً بك في عالم الاحتراف</h1>", unsafe_allow_html=True)
    st.write("##")
    # أزرار مركزية كبيرة
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 دخول التحدي"):
            # هذا الزر ينقلك فوراً للعبة
            st.markdown("""<script>document.querySelector('input[value="🎮 ابدأ التحدي"]').click();</script>""", unsafe_allow_html=True)
            st.info("اختر 'ابدأ التحدي' من القائمة الجانبية")
    with c2:
        if st.button("📚 تصفح القاموس"):
            st.info("اختر 'القاموس الملكي' من القائمة الجانبية")

elif menu == "🎮 ابدأ التحدي":
    st.title(f"🎯 المستوى {st.session_state.lvl}")
    words = levels_dict.get(st.session_state.lvl, levels_dict[1])
    
    if st.button("🔄 كلمة جديدة") or 'game_w' not in st.session_state:
        st.session_state.game_w = random.choice(words)
        st.session_state.time_s = time.time()
        st.rerun()

    rem = max(0, 30 - int(time.time() - st.session_state.time_s))
    st.progress(rem / 30)
    st.write(f"<p style='text-align: center;'>⏳ الوقت: {rem} ثانية</p>", unsafe_allow_html=True)

    if rem > 0:
        eng, arb = st.session_state.game_w.split('-')[0].strip(), st.session_state.game_w.split('-')[1].strip()
        st.markdown(f"<h2 style='background: #0f3460; padding: 20px; border-radius: 10px;'>{eng}</h2>", unsafe_allow_html=True)
        ans = st.text_input("اكتب الترجمة هنا:").strip()
        if st.button("تأكيد ✅"):
            if ans == arb:
                st.balloons()
                st.session_state.score += 20
                if st.session_state.score % 200 == 0:
                    st.session_state.prizes.append(f"وسام المستوى {st.session_state.lvl} 🏅")
                    st.session_state.lvl += 1
                st.success("إجابة صحيحة! +20 نقطة")
            else: st.error(f"خطأ! الحل هو: {arb}")

elif menu == "📖 القاموس الملكي":
    st.title("📖 القاموس الكامل")
    search = st.text_input("🔍 ابحث عن أي كلمة:")
    if search:
        st.table(df_all[df_all['full_line'].str.contains(search, case=False)])
    else:
        st.dataframe(df_all, use_container_width=True, height=500)

# --- 5. الرابط الذي يفتح "كبل" (أسفل القائمة الجانبية) ---
st.sidebar.write("---")
final_url = "https://mohammedqasmkrem-maker.streamlit.app"
share_msg = urllib.parse.quote(f"ادخل كبل على تحدي الـ 1000 كلمة الفخم: {final_url}")
st.sidebar.markdown(f"<a href='https://api.whatsapp.com/send?text={share_msg}' target='_blank'><button style='width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer;'>🟢 ارسل الرابط واتساب</button></a>", unsafe_allow_html=True)
    
