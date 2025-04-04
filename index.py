import streamlit as st
import google.generativeai as genai
import random
import time
import json
import os




# Set up Gemini API Key
API_KEY = "AIzaSyDeo_FSywoTQhoazTFyd-CUslFBuhg8lmM"  # Replace with env var for safety
genai.configure(api_key=API_KEY)

# Persistent history storage file
HISTORY_FILE = "search_history.json"

# Load search history from file
def load_history():
    if os.path.exists("search_history.json") and os.path.getsize("search_history.json") > 0:
        with open("search_history.json", "r") as file:
            return json.load(file)
    else:
        return []  # return an empty list or whatever default you want
with open("search_history.json", "w") as file:
    json.dump([], file)
   

# Save search history to file
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Init history
if "search_history" not in st.session_state:
    st.session_state.search_history = load_history()

# Init theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "light_mode" not in st.session_state:
    st.session_state.light_mode = False

# Dark/light mode
with st.sidebar:
    st.markdown("### 🎨 Theme Settings")
    if st.button("🌙 Toggle Dark/Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.session_state.light_mode = not st.session_state.light_mode
    st.markdown("### 🕵️‍♂️ Recent Searches")
    for name in st.session_state.search_history[-5:][::-1]:
        st.markdown(f"🔸 **{name}**")

# Fonts & Color
bg_color = "#121212" if st.session_state.dark_mode else "#ffffff"
font_color = "#f1f1f1" if st.session_state.dark_mode else "#111"
font_family = "Orbitron"
bg_color = "#0000FF" if st.session_state.light_mode else "#fffggg"
font_color = "#2C2C2C" if st.session_state.light_mode else "#123"
font_family = "Helvetica"

# Add Google Font + Style
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family={font_family}&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {{
        font-family: '{font_family}', sans-serif;
        background-color: {bg_color};
        color: {font_color};
    }}
    .main-container {{
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        background-color: rgba(0, 0, 0, 0.05);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# Gemini call
def get_cricket_player_info(player_name):
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    prompt = f"profile card view  '{player_name}' with stats, teams, achievements, best moments in a readable format."
    response = model.generate_content(prompt)
    return response.text if response and response.text else "No info found."

# App UI
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.title("🏏 Cricket Player Info Finder")
    st.markdown("Enter a cricket player's name to get know of him")

    with st.form("player_form"):
        player_name = st.text_input("🔍 Enter Player Name:")
        submitted = st.form_submit_button("Get Info")

    if submitted and player_name.strip():
        player_name = player_name.strip()
        st.session_state.search_history.append(player_name)
        save_history(st.session_state.search_history)
        with st.spinner(f"🏏 {player_name} is walking to the crease..."):
            st.image("https://i.pinimg.com/originals/1e/ca/09/1eca098c77d3941717b4def514cc6f5f.gif", use_container_width=True)
            time.sleep(2)
            info = get_cricket_player_info(player_name)
        st.success("🏆 Profile Fetched!")
        st.subheader("📋 Player Card")
        with st.expander(f"View {player_name}'s Profile"):
            st.markdown(info, unsafe_allow_html=True)
    elif submitted:
        st.warning("⚠️ Please enter a valid name.")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<footer style='text-align: center; color: gray;'>🏏 Made by BUG SLAYERS </footer>", unsafe_allow_html=True)
