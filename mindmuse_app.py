import streamlit as st
from gtts import gTTS
import base64
import os

# Flashcard Data with Language Attribute
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris", "language": "en"},
    {"question": "What is the square root of 16?", "answer": "4", "language": "en"},
    {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare", "language": "en"},
    {"question": "தமிழில் 'Hello' என்பதற்கான வார்த்தை?", "answer": "வணக்கம்", "language": "ta"},
    {"question": "தமிழில் 'Thank you' என்பதற்கான வார்த்தை?", "answer": "நன்றி", "language": "ta"},
    {"question": "தமிழில் 'Cat' என்பதற்கான வார்த்தை?", "answer": "பூனை", "language": "ta"},
    {"question": "தமிழில் 'Apple' என்பதற்கான வார்த்தை?", "answer": "ஆப்பிள்", "language": "ta"},
    {"question": "'How are you?' தமிழ் மொழியில் என்ன?", "answer": "நீங்கள் எப்படி இருக்கிறீர்கள்?", "language": "ta"},
]

# Initialize Session State
if "index" not in st.session_state:
    st.session_state.index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "question_played" not in st.session_state:
    st.session_state.question_played = False


# Callback Functions
def show_answer():
    st.session_state.show_answer = True

def next_flashcard():
    st.session_state.index = (st.session_state.index + 1) % len(flashcards)
    st.session_state.show_answer = False
    st.session_state.question_played = False


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
    if st.button("Show Answer"):
        show_answer()
        st.rerun()
else:
    st.write(f"**Answer:** {current_card['answer']}")
    #answer_audio = play_audio(current_card["answer"])
    #st.audio(answer_audio)
    answer_audio_file = generate_audio(current_card["answer"], "answer.mp3", current_card["language"])
    answer_audio_html = get_audio_html(answer_audio_file)
    st.markdown(answer_audio_html, unsafe_allow_html=True)

    if st.button("Next"):
        next_flashcard()
        st.rerun()

# Cleanup audio files after use
if os.path.exists("question.mp3"):
    os.remove("question.mp3")
if st.session_state.show_answer and os.path.exists("question.mp3"):
    os.remove("question.mp3")

# Footer
st.write("Powered by MindMuse: Inspired by Athena and the Muses")