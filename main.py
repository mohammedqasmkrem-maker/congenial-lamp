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
    st.markdown("<h2 style='color: #e94560;'>💎 الأكاديمية</h2>
