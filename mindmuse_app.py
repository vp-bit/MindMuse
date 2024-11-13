import streamlit as st
from gtts import gTTS
import base64
import os
import json
import random

# Load flashcards from JSON file
with open("flashcards.json", "r", encoding="utf-8") as f:
    flashcards = json.load(f)

# Shuffle the flashcards for random order
#random.shuffle(flashcards)


# Initialize Session State
if "index" not in st.session_state:
    #st.session_state.index = random.randint(0, len(flashcards) - 1)
    st.session_state.index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "question_played" not in st.session_state:
    st.session_state.question_played = False
if "completed_indices" not in st.session_state:
    st.session_state.completed_indices = []



# Callback Functions
def show_answer():
    st.session_state.show_answer = True

def next_flashcard():
    st.session_state.index = (st.session_state.index + 1) % len(flashcards)
    st.session_state.show_answer = False
    st.session_state.question_played = False

def next_flashcard_rnd():
    # Add current index to completed indices
    st.session_state.completed_indices.append(st.session_state.index)

    # Check if all flashcards have been shown
    if len(st.session_state.completed_indices) == len(flashcards) - 1:
        st.session_state.completed_indices = []  # Reset when all are completed
        st.session_state.completed_indices.append(0)

    # Select a new random index that hasn’t been shown yet
    remaining_indices = [i for i in range(len(flashcards)) if i not in st.session_state.completed_indices]
    st.session_state.index = random.choice(remaining_indices)
    st.session_state.show_answer = False
    st.session_state.question_played = False
    st.rerun()


def play_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file = f"audio_{st.session_state.index}.mp3"
    tts.save(audio_file)
    return audio_file


def generate_audio(text, filename, language):
    tts = gTTS(text=text, lang=language)
    tts.save(filename)
    return filename


def get_audio_html(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        return audio_html


# App Title
current_card = flashcards[st.session_state.index]
st.title("MindMuse: Your Learning Companion")

# Sidebar for Navigation (we can expand this later)
st.sidebar.title("Explore MindMuse")
st.sidebar.selectbox("Choose a Category", ["General Knowledge", "Math", "Literature"])

# Display Current Flashcard
current_card = flashcards[st.session_state.index]


# Play question audio
#question_audio = play_audio(current_card["question"])
#st.audio(question_audio)
if not st.session_state.question_played:
    question_audio_file = generate_audio(current_card["question"], "question.mp3", current_card["language"])
    question_audio_html = get_audio_html(question_audio_file)
    st.markdown(question_audio_html, unsafe_allow_html=True)
    st.session_state.question_played = True
st.subheader(current_card["question"])



if not st.session_state.show_answer:
    if st.button("Get Started" if st.session_state.index == 0 else "Show Answer"):
            show_answer()
            st.rerun()
else:
    st.markdown(f"<h2 style='font-size: 32px; font-weight: bold; color: #333;'>{current_card['answer']}</h2>", unsafe_allow_html=True)
    if "phonetic_answer" in current_card:
        st.markdown(f"<h3 style='font-size: 48px; font-weight: bold; color: #555;'>{current_card['phonetic_answer']}</h3>", unsafe_allow_html=True)
    #answer_audio = play_audio(current_card["answer"])
    #st.audio(answer_audio)
    answer_audio_file = generate_audio(current_card["answer"], "answer.mp3", current_card["language"])
    answer_audio_html = get_audio_html(answer_audio_file)
    st.markdown(answer_audio_html, unsafe_allow_html=True)

    if st.button("Next"):
        next_flashcard_rnd()
        st.rerun()

# Cleanup audio files after use
if os.path.exists("question.mp3"):
    os.remove("question.mp3")
if st.session_state.show_answer and os.path.exists("question.mp3"):
    os.remove("question.mp3")

# Footer
st.write("Powered by MindMuse: Inspired by Atheena and the Muses")