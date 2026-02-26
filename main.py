import streamlit as st
import pandas as pd
import random
import os
import urllib.parse
import time

# إعداد الصفحة
st.set_page_config(page_title="أكاديمية الـ 1000 كلمة", layout="wide")

# 1. تحميل البيانات
@st.cache_data
def load_data():
    file_name = 'vocab.csv'
    if os.path.exists(file_name):
        df = pd.read_csv(file_name, header=None, names=['full_line'], sep='|', engine='python')
        df['level'] = 'سهل'
        if len(df) > 300: df.loc[300:700, 'level'] = 'متوسط'
        if len(df) > 700: df.loc[700:, 'level'] = 'صعب'
        return df
    return None

df = load_data()

# 2. إدارة الحالة (Session State)
if 'score' not in st.session_state: st.session_state.score = 0
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# 3. القائمة الجانبية (المشاركة والروابط المصلحة)
st.sidebar.title("🚀 لوحة التحكم")
st.sidebar.metric("نقاطك 🏆", st.session_state.score)

# --- إصلاح روابط المشاركة ---
# ملاحظة: ضع رابط تطبيقك الحقيقي هنا بدل الرابط أدناه
my_actual_url = "https://your-app-link.streamlit.app" 
share_msg = f"جمعت {st.session_state.score} نقطة في تحدي الكلمات! جرب مستواك: {my_actual_url}"
encoded_msg = urllib.parse.quote(share_msg)

st.sidebar.subheader("📢 انشر التحدي")
# روابط مباشرة ومختصرة لضمان الفتح
st.sidebar.markdown(f"**[✈️ انشر عبر تليجرام](https://t.me/share/url?url={my_actual_url}&text={encoded_msg})**")
st.sidebar.markdown(f"**[🟢 انشر عبر واتساب](https://api.whatsapp.com/send?text={encoded_msg})**")

menu = st.sidebar.radio("القائمة:", ["🎮 التحدي الزمني", "📖 القاموس"])

# 4. محتوى التطبيق
if df is not None:
    if menu == "🎮 التحدي الزمني":
        st.title("⏱️ تحدي الثواني العشر!")
        lvl = st.selectbox("المستوى:", ["سهل", "متوسط", "صعب"])
        level_df = df[df['level'] == lvl]

        if st.button("كلمة جديدة 🔄"):
            st.session_state.current_item = random.choice(level_df['full_line'].values)
            st.session_state.start_time = time.time() 
            st.rerun()

        if 'current_item' in st.session_state:
            # حساب الوقت المتبقي
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, 10 - int(elapsed))
            
            if remaining > 0:
                st.write(f"⏳ الوقت المتبقي: **{remaining}** ثانية")
                # شريط تقدم للوقت
                st.progress(remaining / 10)
            else:
                st.error("⏰ انتهى الوقت! اضغط 'كلمة جديدة' للتعويض.")

            item = st.session_state.current_item
            eng = item.split('-')[0].strip() if '-' in item else item
            arb = item.split('-')[1].strip() if '-' in item else "غير مترجم"

            st.info(f"### ما معنى الكلمة التالية بالعربي؟ \n # {eng}")
            
            user_ans = st.text_input("اكتب الجواب هنا:", key="ans_input").strip()

            if st.button("تحقق ✅"):
                if remaining == 0:
                    st.warning("انتهى الوقت، لم تُحسب النقاط!")
                elif user_ans == arb:
                    st.success(f"صح! أحسنت 💪 (+20 نقطة)")
                    st.session_state.score += 20
                    st.balloons()
                else:
                    st.error(f"خطأ! الجواب هو: {arb}")

    elif menu == "📖 القاموس":
        st.title("📖 القاموس الذكي")
        search = st.text_input("بحث:")
        res = df[df['full_line'].str.contains(search, case=False)] if search else df
        st.dataframe(res[['level', 'full_line']], use_container_width=True)

else:
    st.error("الملف غير موجود")
