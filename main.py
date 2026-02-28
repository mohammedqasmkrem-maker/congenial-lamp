import streamlit as st
import sqlite3
import random
import time
from gtts import gTTS
import uuid
import os

st.set_page_config(page_title="Vocabulary Quiz Pro", page_icon="🏆")

# =========================
# Database Setup
# =========================
conn = sqlite3.connect("scores.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    name TEXT,
    score INTEGER
)
""")
conn.commit()

# =========================
# Dictionary
# =========================
words = {
    "كتاب": "book",
    "قلم": "pen",
    "شجرة": "tree",
    "مدرسة": "school",
    "سيارة": "car",
    "جامعة": "university",
    "مكتبة": "library"
}

# =========================
# Session State
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(words.items()))

if "repeat_used" not in st.session_state:
    st.session_state.repeat_used = False

if "time_left" not in st.session_state:
    st.session_state.time_left = 15

if "name" not in st.session_state:
    st.session_state.name = ""

# =========================
# Audio Function
# =========================
def play_audio(text):
    tts = gTTS(text=text, lang='en')
    filename = f"temp_{uuid.uuid4()}.mp3"
    tts.save(filename)
    audio_file = open(filename, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
    st.audio(audio_bytes)
    os.remove(filename)

# =========================
# Header
# =========================
st.title("🏆 Professional Vocabulary Quiz")

st.session_state.name = st.text_input("👤 Enter your name")

st.markdown(f"### 🎯 Score: {st.session_state.score}")
st.markdown(f"### ⏳ Time Left: {st.session_state.time_left}")

st.divider()

# =========================
# Show Word
# =========================
arabic, english = st.session_state.current_word

st.markdown(
    f"<h2 style='text-align:center; color:green;'>{arabic}</h2>",
    unsafe_allow_html=True
)

play_audio(english)

# =========================
# Input
# =========================
answer = st.text_input("✍️ Write English word")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Submit"):
        if answer.lower().strip() == english:
            st.success("Correct ✅")
            st.session_state.score += 10
            st.session_state.current_word = random.choice(list(words.items()))
            st.session_state.repeat_used = False
            st.session_state.time_left = 15
            st.rerun()
        else:
            st.error("Wrong ❌ Try again")

with col2:
    if st.button("💡 Hint"):
        st.info(f"First letter: {english[0]}")

with col3:
    if st.button("🔁 Repeat"):
        if not st.session_state.repeat_used:
            play_audio(english)
            st.session_state.repeat_used = True
        else:
            st.error("Repeat already used!")

# =========================
# Timer
# =========================
time.sleep(1)
st.session_state.time_left -= 1

if st.session_state.time_left <= 0:
    st.warning("⏰ Time's up!")
    st.session_state.current_word = random.choice(list(words.items()))
    st.session_state.time_left = 15
    st.rerun()

# =========================
# Save Score
# =========================
if st.button("💾 Save Score"):
    if st.session_state.name != "":
        c.execute("INSERT INTO leaderboard VALUES (?, ?)",
                  (st.session_state.name, st.session_state.score))
        conn.commit()
        st.success("Score Saved!")
    else:
        st.error("Enter your name first!")

# =========================
# Leaderboard
# =========================
st.divider()
st.subheader("🏅 Top Players")

c.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 5")
top_players = c.fetchall()

for player in top_players:
    st.write(f"{player[0]} — {player[1]} points")

# =========================
# Reset
# =========================
if st.button("🔄 Reset Game"):
    st.session_state.score = 0
    st.session_state.current_word = random.choice(list(words.items()))
    st.session_state.time_left = 15
    st.session_state.repeat_used = False
    st.rerun()

# =========================
# Footer
# =========================
st.markdown("""
---
🔗 My Streamlit App:  
https://share.streamlit.io/user/mqasmkrem-a11y
""")
