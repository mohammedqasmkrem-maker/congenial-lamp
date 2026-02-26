import streamlit as st
import pandas as pd
import random
import os
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="أكاديمية المستويات", layout="wide")

# 2. تحميل البيانات وتنظيمها في مستويات (100 كلمة لكل مستوى)
@st.cache_data
def load_and_split_data():
    if os.path.exists('vocab.csv'):
        df = pd.read_csv('vocab.csv', header=None, names=['full_line'], sep='|', engine='python')
    else:
        # كلمات تجريبية في حال عدم وجود الملف
        data = [f"Word {i} - كلمة {i}" for i in range(1, 301)]
        df = pd.DataFrame({'full_line': data})
    
    # تقسيم الكلمات إلى مجموعات (كل مجموعة 100)
    levels = {}
    for i in range(0, len(df), 100):
        lvl_num = (i // 100) + 1
        levels[lvl_num] = df['full_line'].iloc[i:i+100].values
    return df, levels

df_all, levels_dict = load_and_split_data()

# 3. إدارة الحالة (Session State)
if 'score' not in st.session_state: st.session_state.score = 0
if 'prizes' not in st.session_state: st.session_state.prizes = []
if 'current_level' not in st.session_state: st.session_state.current_level = 1

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("🏆 لوحة التحكم")
    menu = st.radio("انتقل إلى:", ["🏠 الرئيسية", "🎮 اختبار المستويات", "📖 القاموس الكامل", "🏅 الجوائز"])
    
    st.write("---")
    st.write(f"**المستوى الحالي:** {st.session_state.current_level}")
    st.metric("مجموع النقاط 🏆", st.session_state.score)

# --- 5. محتوى الصفحات ---

if menu == "🏠 الرئيسية":
    st.title("👋 مرحباً بك في نظام المستويات")
    st.write(f"يحتوي التطبيق حالياً على **{len(levels_dict)} مستويات**. كل مستوى يضم 100 كلمة.")
    st.info("انتقل إلى 'اختبار المستويات' لتبدأ التحدي وتحصل على الجوائز!")

elif menu == "🎮 اختبار المستويات":
    st.title(f"🎯 التحدي: المستوى {st.session_state.current_level}")
    
    # اختيار كلمة من المستوى الحالي فقط
    current_lv_words = levels_dict.get(st.session_state.current_level, levels_dict[1])
    
    if st.button("🔄 كلمة جديدة") or 'game_word' not in st.session_state:
        st.session_state.game_word = random.choice(current_lv_words)
        st.session_state.start_t = time.time()
        st.rerun()

    rem = max(0, 30 - int(time.time() - st.session_state.start_t))
    st.progress(rem / 30)
    
    word_line = st.session_state.game_word
    eng, arb = word_line.split('-')[0].strip(), word_line.split('-')[1].strip()
    
    st.subheader(f"ما معنى: **{eng}**؟")
    ans = st.text_input("أدخل الإجابة بالعربي:", key="ans_input").strip()
    
    if st.button("تحقق ✅"):
        if ans == arb:
            st.success("إجابة صحيحة! +20 نقطة")
            st.session_state.score += 20
            
            # نظام الجوائز والترقية للمستوى التالي
            if st.session_state.score > 0 and st.session_state.score % 200 == 0: # مثال: كل 200 نقطة جائزة
                prize_name = f"وسام إتمام المستوى {st.session_state.current_level} 🥇"
                if prize_name not in st.session_state.prizes:
                    st.session_state.prizes.append(prize_name)
                    st.balloons()
                    st.session_state.current_level += 1 # الترقية للمستوى التالي
                    st.info(f"تهانينا! انتقلت إلى المستوى {st.session_state.current_level}")
        else:
            st.error(f"خطأ! الجواب هو: {arb}")

elif menu == "📖 القاموس الكامل":
    st.title("📖 القاموس الشامل")
    search = st.text_input("🔍 ابحث عن كلمة معينة أو تصفح الكل:")
    
    if search:
        results = df_all[df_all['full_line'].str.contains(search, case=False)]
        st.table(results)
    else:
        st.write("عرض كافة الكلمات في قاعدة البيانات:")
        st.dataframe(df_all, use_container_width=True, height=400)

elif menu == "🏅 الجوائز":
    st.title("🏅 خزانة الجوائز")
    if not st.session_state.prizes:
        st.warning("لم تربح أي جوائز بعد. استمر في الاختبار لترقية مستواك!")
    else:
        for p in st.session_state.prizes:
            st.success(f"🎊 {p}")
        
