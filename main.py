import streamlit as st
import pandas as pd
import random
import os
import time
import urllib.parse

# 1. إعدادات التصميم الفخم
st.set_page_config(page_title="أكاديمية اللغة الملكية", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; }
    h1 { color: #e94560 !important; text-align: center; font-family: 'Arial'; }
    div.stButton > button { 
        background-color: #e94560; color: white; border-radius: 12px; 
        height: 60px; font-weight: bold; width: 100%; border: none;
    }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات وتنظيم المستويات
@st.cache_data
def load_and_organize():
    if os.path.exists('vocab.csv'):
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    else:
        df = pd.DataFrame({'full_line': [f"Word {i} - كلمة {i}" for i in range(1, 1001)]})
    
    # تقسيم الكلمات إلى مستويات (100 كلمة لكل مستوى)
    lvls = { (i // 100) + 1 : df['full_line'].iloc[i:i+100].values for i in range(0, len(df), 100) }
    return df, lvls

df_all, levels_dict = load_and_organize()

# إدارة الحالة (Session State)
if 'score' not in st.session_state: st.session_state.score = 0
if 'lvl' not in st.session_state: st.session_state.lvl = 1
if 'correct_count' not in st.session_state: st.session_state.correct_count = 0

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color: #e94560;'>💎 الأكاديمية</h2>", unsafe_allow_html=True)
    menu = st.radio("القائمة:", ["🏠 الرئيسية", "🎮 التحدي التفاعلي", "📖 القاموس المبوب", "🏆 الجوائز"])
    st.write("---")
    st.metric("نقاطك", st.session_state.score)
    st.write(f"المستوى الحالي: {st.session_state.lvl}")
    
    # --- الرابط الذي طلبته للمشاركة ---
    st.write("---")
    app_url = "https://mohammedqasmkrem-maker.streamlit.app"
    share_text = urllib.parse.quote(f"جرب تحدي الـ 1000 كلمة الملكي! ادخل كبل من هنا: {app_url}")
    st.markdown(f"""
        <a href="https://api.whatsapp.com/send?text={share_text}" target="_blank">
            <button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer;">
                🟢 شارك الرابط واتساب
            </button>
        </a>
    """, unsafe_allow_html=True)

# --- 4. محتوى الصفحات ---

if menu == "🏠 الرئيسية":
    st.markdown("<h1>👑 مرحباً بك في عالم الاحتراف</h1>", unsafe_allow_html=True)
    st.write("تطبيقك جاهز الآن مع نظام مستويات وقاموس مبوب.")
    st.info(f"رابط تطبيقك للنشر: {app_url}")

elif menu == "🎮 التحدي التفاعلي":
    st.title(f"🎯 المستوى {st.session_state.lvl}")
    words = levels_dict.get(st.session_state.lvl, levels_dict[1])
    
    # اختيار كلمة جديدة تلقائياً إذا لم تكن موجودة
    if 'game_word' not in st.session_state:
        st.session_state.game_word = random.choice(words)
        st.session_state.start_time = time.time()

    rem = max(0, 30 - int(time.time() - st.session_state.start_time))
    st.progress(rem / 30)
    
    eng, arb = st.session_state.game_word.split('-')[0].strip(), st.session_state.game_word.split('-')[1].strip()
    st.subheader(f"ما معنى: {eng}؟")
    
    # خانة الإجابة مع ميزة التغيير التلقائي
    user_ans = st.text_input("أدخل الترجمة واضغط Enter:", key=f"input_{st.session_state.correct_count}").strip()
    
    if user_ans:
        if user_ans == arb:
            st.success("✅ صحيح! جارٍ الانتقال للكلمة التالية...")
            st.session_state.score += 20
            st.session_state.correct_count += 1
            # تغيير الكلمة فوراً وبشكل آلي
            st.session_state.game_word = random.choice(words)
            st.session_state.start_time = time.time()
            
            # ترقية المستوى كل 10 إجابات صحيحة
            if st.session_state.correct_count % 10 == 0:
                st.session_state.lvl += 1
                st.balloons()
            
            time.sleep(1) # تأخير بسيط ليرى المستخدم كلمة "صحيح"
            st.rerun()
        else:
            st.error(f"❌ خطأ! الجواب الصحيح هو: {arb}")

elif menu == "📖 القاموس المبوب":
    st.title("📖 القاموس الملكي (صفحات)")
    
    # القاموس على شكل صفحات
    words_per_page = 20
    total_pages = len(df_all) // words_per_page
    page_num = st.number_input("الصفحة", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page_num - 1) * words_per_page
    end_idx = start_idx + words_per_page
    
    st.table(df_all.iloc[start_idx:end_idx])

elif menu == "🏆 الجوائز":
    st.title("🏆 إنجازاتك")
    st.write(f"لقد جمعت {st.session_state.score} نقطة وتجاوزت {st.session_state.lvl - 1} مستويات!")
    
