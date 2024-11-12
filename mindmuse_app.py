import streamlit as st

# Flashcard Data: Feel free to expand this list!
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the square root of 16?", "answer": "4"},
    {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare"},
]

# Initialize Session State
if "index" not in st.session_state:
    st.session_state.index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# Callback Functions
def show_answer():
    st.session_state.show_answer = True

def next_flashcard():
    st.session_state.index = (st.session_state.index + 1) % len(flashcards)
    st.session_state.show_answer = False

# App Title
st.title("MindMuse: Your Learning Companion")

# Sidebar for Navigation (we can expand this later)
st.sidebar.title("Explore MindMuse")
st.sidebar.selectbox("Choose a Category", ["General Knowledge", "Math", "Literature"])

# Display Current Flashcard
current_card = flashcards[st.session_state.index]
st.subheader(current_card["question"])

if not st.session_state.show_answer:
    if st.button("Show Answer"):
        show_answer()
        st.rerun()
else:
    st.write(f"**Answer:** {current_card['answer']}")
    if st.button("Next"):
        next_flashcard()
        st.rerun()



# Footer
st.write("Powered by MindMuse: Inspired by Athena and the Muses")