import streamlit as st
from gtts import gTTS
import base64
import os
import json
import random
import tempfile
import pandas as pd
from io import StringIO


def generate_audio(text, language):
    try:
        tts = gTTS(text=text, lang=language)
        #use temp file to keep unique version per user
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            temp_file_path = temp_file.name
    except Exception as e:
        st.error(f"Failed to generate audio: {e}")
        return

    return  temp_file_path 


def autoplay_audio(file_path: str, auto_play):
    if auto_play:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=auto_play,
            )

    else:
        st.audio(file_path, format="audio/mp3")

def safe_delete(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        st.error("Error deleting file: {e}")

@st.cache_data
def load_flashcards_f_file(uploaded_file):
    if uploaded_file is None:
    #Load from default JSon file
        with open("flashcards.json", "r", encoding="utf-8") as f:
            return json.load(f)  
    else: 
        # read file as string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return json.load(stringio)  

# Internal Functions
def set_question_state(flag: bool):
    st.session_state.question_viewed = flag

def set_answer_state(flag: bool):
    st.session_state.answer_viewed = flag

def set_current_card(index: int):
    st.session_state.index = index
    set_question_state(False)
    set_answer_state(False)
    if index == -1:
        st.session_state.question_audio_file = generate_audio("Let's get started", "en")
        st.session_state.answer_audio_file = generate_audio("Welcome!", "en")
    else:
        current_card = st.session_state.selected_cards[index]
        st.session_state.current_card = current_card
        st.session_state.question_audio_file = generate_audio(current_card["question"], current_card["language"])
        st.session_state.answer_audio_file = generate_audio(current_card["answer"], current_card["language"])

def next_flashcard():
    set_current_card(st.session_state.index + 1)

def filter_by_value(el: list,category: str,source: str,level:str):
    selected_cards = el
    if not category=="All" and source=="All" and level=="All": 
        selected_cards = [card for card in el if (category=="All" or card["category"] == category) and (level=="All" or card["level"] == level)]
    return selected_cards 

def load_cards(category,source,level):
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = load_flashcards_f_file(None)

    flashcards = st.session_state.flashcards 
    
    #Populate drop downs with available attributes
    st.session_state.categories = list(set(card["category"] for card in flashcards))
    st.session_state.categories.insert(0, "All")  # Add an 'All' option to show all flashcards
    st.session_state.levels = list(set(card["level"] for card in flashcards))
    st.session_state.levels.insert(0, "All")  # Add an 'All' option to show all flashcards
    st.session_state.sources = list(set(card["source"] for card in flashcards))
    st.session_state.sources.insert(0, "All")  # Add an 'All' option to show all flashcards (multiple per card?)

    #Filter by selection
    selected_cards = filter_by_value(flashcards,category,source,level)
    random.shuffle(selected_cards)
    st.session_state.selected_cards = selected_cards

    #Initialize
    set_current_card(-1)


# Initialize Session State
if "selected_cards" not in st.session_state:
    load_cards("All","All","All")

# App Title
st.title("MindMuse: Your Learning Companion")

# Sidebar for Navigation (we can expand this later)
st.sidebar.title("Explore MindMuse")
selected_categories = st.sidebar.selectbox("Choose a Category", st.session_state.categories)
selected_sources = st.sidebar.selectbox("Choose a Source", st.session_state.sources)
selected_levels = st.sidebar.selectbox("Choose your Level", st.session_state.levels)
if st.sidebar.button("Select Content"):
    load_cards(selected_categories,selected_sources,selected_levels)
    st.rerun()

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.session_state.flashcards = load_flashcards_f_file(uploaded_file)
    load_cards("All","All","All")    
    st.rerun()    

# Initial Screen
if st.session_state.index == -1:
    st.subheader("Muses are getting warmed up")
else:
    current_card = st.session_state.current_card
    st.subheader(current_card["question"])
    autoplay_audio(st.session_state.question_audio_file,not st.session_state.question_viewed)
    set_question_state(True)

    if not st.session_state.answer_viewed:
        if st.button("Show Answer"):
                set_answer_state(True)
                st.rerun()
    else:
        st.markdown(f"<h2 style='font-size: 32px; font-weight: bold; color: #333;'>{current_card['answer']}</h2>", unsafe_allow_html=True)
        if "phonetic_answer" in current_card:
            st.markdown(f"<h3 style='font-size: 48px; font-weight: bold; color: #555;'>{current_card['phonetic_answer']}</h3>", unsafe_allow_html=True)
        autoplay_audio(st.session_state.answer_audio_file,True)

if st.button("Next"):
    safe_delete(st.session_state.question_audio_file)
    safe_delete(st.session_state.answer_audio_file)
    next_flashcard()
    st.rerun()


# Footer
st.write("Powered by MindMuse: Inspired by Atheena and the Muses")