import streamlit as st
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import random
import json
from datetime import datetime, timedelta
import requests

# Set page config (first Streamlit command)
st.set_page_config(page_title="Advanced Gemini Learning Companion", layout="wide")

# API keys (replace with your actual API keys)
GEMINI_API_KEY = 'AIzaSyDP2hi6e7XW97hVPiT1LNZt_cj6IdijXRQ'
YOUTUBE_API_KEY = 'AIzaSyAPoUwwPHqytoo258chZ4RA4N0dK55mbWQ'
BOOK_API_KEY = 'AIzaSyBAkXKsLQHOg99KnTox11a58YLPSLExLec'
# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Set safety settings
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "name": "Student",
        "subjects": [],
        "learning_style": "",
        "difficulty_level": 3,
        "points": 0,
        "badges": [],
        "completed_quizzes": 0,
        "average_score": 0,
    }
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = ""
if 'study_plan' not in st.session_state:
    st.session_state.study_plan = {}

    # Function to get response from Gemini API


def get_gemini_response(query, chat_history):
    try:
        response = model.generate_content(
            f"User Profile: {json.dumps(st.session_state.user_profile)}\n\nChat History: {json.dumps(chat_history)}\n\nUser Query: {query}",
            safety_settings=safety_settings,
            generation_config={
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            },
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


# Function to generate personalized study plan
# Function to generate personalized study plan
# Function to generate personalized study plan (in text format)
# Function to generate personalized study plan (in plain text format)
def generate_study_plan(subject):
    prompt = f"""
    Create a personalized study plan for {st.session_state.user_profile['name']} to learn about {subject}.
    Consider the following:
    - Learning style: {st.session_state.user_profile['learning_style']}
    - Difficulty level: {st.session_state.user_profile['difficulty_level']}
    - Previous subjects studied: {', '.join(st.session_state.user_profile['subjects'])}

    For each day, include:
    1. Main topic to cover
    2. Subtopics or concepts
    3. Recommended learning activities (based on learning style)
    4. Suggested resources (e.g., book chapters, video tutorials)
    5. Practice exercises or assignments

    Present the plan in clear, readable plain text.
    """
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text  # Return plain text instead of JSON

    except Exception as e:
        return f"Error generating study plan: {str(e)}"


# Function to generate quiz questions
# Function to generate quiz questions
# Function to generate quiz questions
# Function to generate quiz questions (in text format)
# Function to generate quiz questions (in plain text format)
def generate_quiz(subject, difficulty):
    prompt = f"""
    Generate 5 multiple-choice quiz questions about {subject} at difficulty level {difficulty}.
    For each question, provide:
    1. The question text
    2. Four answer options (A, B, C, D)
    3. The correct answer letter
    4. A brief explanation of the correct answer

    Present the quiz as plain text in a clean, readable format.
    """
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text  # Return plain text response

    except Exception as e:
        return f"Error generating quiz: {str(e)}"


# Function to simplify complex concepts
def simplify_concept(concept, difficulty):
    prompt = f"""
    Explain the concept of '{concept}' in simple terms, suitable for a student at difficulty level {difficulty}.
    Include:
    1. A brief definition
    2. Key points to understand
    3. An everyday analogy or example
    4. A simple diagram or visualization (described in text)
    """
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text
    except Exception as e:
        return f"Error simplifying concept: {str(e)}"


# Function to get learning resources
def get_learning_resources(subject):
    # YouTube videos
    videos = get_youtube_videos(subject)

    # Books
    books = get_books(subject)

    # Generate additional resource suggestions using Gemini
    prompt = f"Suggest 3 interactive online learning modules or simulations for studying {subject}."
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        interactive_resources = response.text.split('\n')
    except Exception as e:
        interactive_resources = [f"Error fetching interactive resources: {str(e)}"]

    return {
        "videos": videos,
        "books": books,
        "interactive_resources": interactive_resources
    }


# Function to update user profile
def update_user_profile(subject, quiz_score):
    if subject not in st.session_state.user_profile['subjects']:
        st.session_state.user_profile['subjects'].append(subject)
    st.session_state.user_profile['completed_quizzes'] += 1
    st.session_state.user_profile['points'] += quiz_score * 10
    total_score = st.session_state.user_profile['average_score'] * (
                st.session_state.user_profile['completed_quizzes'] - 1) + quiz_score
    st.session_state.user_profile['average_score'] = total_score / st.session_state.user_profile['completed_quizzes']

    # Check for new badges
    if st.session_state.user_profile['completed_quizzes'] == 5:
        st.session_state.user_profile['badges'].append("Quiz Master")
    if st.session_state.user_profile['points'] >= 1000:
        st.session_state.user_profile['badges'].append("Point Collector")


# Main Streamlit app
st.title("Advanced Gemini-Powered AI Learning Companion")

# Sidebar for user profile and preferences
st.sidebar.title("User Profile")
st.session_state.user_profile['name'] = st.sidebar.text_input("Your Name",
                                                               key="user_name",  # Unique key for name
                                                               value=st.session_state.user_profile['name'])
st.session_state.user_profile['learning_style'] = st.sidebar.selectbox("Learning Style",
                                                                       ["Visual", "Auditory", "Reading/Writing",
                                                                        "Kinesthetic"],
                                                                       index=["Visual", "Auditory", "Reading/Writing",
                                                                              "Kinesthetic"].index(
                                                                           st.session_state.user_profile[
                                                                               'learning_style']) if
                                                                       st.session_state.user_profile[
                                                                           'learning_style'] else 0,
                                                                       key="learning_style")  # Unique key for style
st.session_state.user_profile['difficulty_level'] = st.sidebar.slider("Difficulty Level", 1, 5,
                                                                      st.session_state.user_profile['difficulty_level'],
                                                                      key="difficulty_level")  # Unique key for slider

# Function to get YouTube videos (get_youtube_videos):

def get_youtube_videos(subject):
    """
    This function retrieves relevant YouTube videos for a given subject using the YouTube Data API.

    Args:
        subject: The subject to search for videos on (string).

    Returns:
        A list of tuples, where each tuple contains the video title and URL.
    """
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={subject}+tutorial&type=video&key={YOUTUBE_API_KEY}"

    try:
        response = requests.get(search_url)
        data = response.json()
        videos = []

        for item in data.get('items', []):
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append((video_title, video_url))

        return videos

    except Exception as e:
        return [f"Error fetching YouTube videos: {str(e)}"]


# Function to Get Books (get_books):






def get_books(subject, GOOGLE_BOOKS_API_KEY=BOOK_API_KEY):
    """
    This function retrieves suggested books related to a given subject using the Google Books API.

    Args:
        subject: The subject to search for books on (string).

    Returns:
        A list of book titles (strings) or an error message.
    """
    google_books_url = f"https://www.googleapis.com/books/v1/volumes?q={subject}&key={GOOGLE_BOOKS_API_KEY}"

    try:
        response = requests.get(google_books_url)
        data = response.json()

        books = []
        # Extracting book titles from the API response
        for item in data.get('items', []):
            book_title = item['volumeInfo'].get('title', 'No Title Available')
            books.append(book_title)
            if len(books) == 3:  # Limit to top 3 books
                break

        return books

    except Exception as e:
        return [f"Error fetching books: {str(e)}"]


# Main Streamlit app
st.title("Advanced Gemini-Powered AI Learning Companion")

# Sidebar for user profile and preferences
st.sidebar.title("User Profile")
st.session_state.user_profile['name'] = st.sidebar.text_input("Your Name", st.session_state.user_profile['name'])
st.session_state.user_profile['learning_style'] = st.sidebar.selectbox("Learning Style",
                                                                       ["Visual", "Auditory", "Reading/Writing",
                                                                        "Kinesthetic"],
                                                                       index=["Visual", "Auditory", "Reading/Writing",
                                                                              "Kinesthetic"].index(
                                                                           st.session_state.user_profile[
                                                                               'learning_style']) if
                                                                       st.session_state.user_profile[
                                                                           'learning_style'] else 0)
st.session_state.user_profile['difficulty_level'] = st.sidebar.slider("Difficulty Level", 1, 5,
                                                                      st.session_state.user_profile['difficulty_level'])

# Display user stats
st.sidebar.write("---")
st.sidebar.write("### Your Stats")
st.sidebar.write(f"Points: {st.session_state.user_profile['points']}")
st.sidebar.write(f"Badges: {', '.join(st.session_state.user_profile['badges'])}")
st.sidebar.write(f"Quizzes Completed: {st.session_state.user_profile['completed_quizzes']}")
st.sidebar.write(f"Average Score: {st.session_state.user_profile['average_score']:.2f}%")

# Main learning interface
st.write("Welcome to your personalized learning journey! What would you like to study today?")

# Subject selection
subject_options = ["Mathematics", "Science", "History", "Literature", "Computer Science", "Languages"]
st.session_state.current_subject = st.selectbox("Choose a subject", [""] + subject_options)

if st.session_state.current_subject:
    # Generate or display study plan
    # Study Plan Display
    # Display Study Plan
    if st.button("Generate Study Plan") or st.session_state.current_subject not in st.session_state.study_plan:
        study_plan_text = generate_study_plan(st.session_state.current_subject)
        st.write("### Your Personalized Study Plan")
        st.text(study_plan_text)  # Display as plain text

    # Display Quiz
    if st.button("Take a Quiz"):
        quiz_text = generate_quiz(st.session_state.current_subject, st.session_state.user_profile['difficulty_level'])
        st.write("### Quick Quiz")
        st.text(quiz_text)  # Display quiz as plain text
    # Learning resources
    st.write("### Learning Resources")
    resources = get_learning_resources(st.session_state.current_subject)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("*YouTube Videos:*")
        for title, url in resources['videos']:
            st.write(f"- [{title}]({url})")

    with col2:
        st.write("*Recommended Books:*")
        for book in resources['books']:
            st.write(f"- {book}")

    with col3:
        st.write("*Interactive Resources:*")
        for resource in resources['interactive_resources']:
            st.write(f"- {resource}")

    # Concept simplification
    st.write("### Concept Simplification")
    concept = st.text_input("Enter a concept you'd like simplified:")
    if concept:
        simplified_explanation = simplify_concept(concept, st.session_state.user_profile['difficulty_level'])
        st.write(simplified_explanation)

    # Quiz


# Chat interface
st.write("### Chat with Your AI Tutor")
query = st.text_input("Ask a question about your studies:")
if st.button("Send"):
    if query:
        response = get_gemini_response(query, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({"role": "ai", "content": response})

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.write(f"*You:* {message['content']}")
    else:
        st.write(f"*AI Tutor:* {message['content']}")

# Gamification elements
if st.session_state.user_profile['points'] > 0:
    st.sidebar.write("---")
    st.sidebar.write("### Learning Challenges")
    challenge = st.sidebar.selectbox("Select a challenge:", ["Complete 3 quizzes this week", "Study for 2 hours today",
                                                             "Explain a concept to a friend"])
    if st.sidebar.button("Accept Challenge"):
        st.sidebar.success(f"Challenge accepted! Complete '{challenge}' to earn extra points and badges!")

# Collaborative learning (simulated)
st.sidebar.write("---")
st.sidebar.write("### Collaborative Learning")
if st.sidebar.button("Join a Study Group"):
    st.sidebar.info("You've joined a study group for Advanced Mathematics. Next session: Tomorrow at 3 PM.")

# Motivational messages
motivation_messages = [
    "Great job on your progress! Keep it up!",
    "Remember, every bit of studying counts towards your goals!",
    "You're doing fantastic! How about taking a quick quiz to test your knowledge?",
    "Learning is a journey, and you're making great strides!",
]
st.sidebar.write("---")
st.sidebar.write