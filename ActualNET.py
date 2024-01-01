import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import anakytics

st.session_state.started = False
st.session_state.quizComplete = False
st.session_state.mcqloop = False
st.session_state.num = 0

if 'num' not in st.session_state:
    st.session_state.num = 0

if 'mcq_list' not in st.session_state:
    st.session_state.mcq_list = []


def fetch_mcqs(num_mcqs, subject):
    api_endpoint = "http://localhost:5000/mcq/get_mcqs"
    params = {"num_mcqs": num_mcqs, "subject": subject}

    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            mcqs = response.json()["mcqs"]
            return mcqs
        else:
            st.error(f"Error fetching MCQs: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error fetching MCQs: {str(e)}")
        return None


def create_quiz(num_mcqs, subject):
    api_endpoint = "http://localhost:5000/quiz/create_quiz"
    try:
        jsondata = {
            'uuid': st.session_state.uuid,
            'quizType': 'MCQ',
            'quizSubject': subject,
            'quizTotalMcqs': num_mcqs,
        }
        response = requests.post(api_endpoint, json=jsondata)
        if response.status_code == 200:
            st.success("Quiz created successfully!")
            # fetch the quiz id
            quiz_id = response.json()["quizid"]
            st.session_state.quiz_id = quiz_id
        else:
            st.error(f"Error creating quiz: {response.text}")
    except Exception as e:
        st.error(f"Error creating quiz: {str(e)}")


def submit_quiz(num_correct):
    api_endpoint = "http://localhost:5000/quiz/submit_quiz"

    try:
        jsondata = {
            'uuid': st.session_state.uuid,
            'quizid': st.session_state.quiz_id,
            'correctOptions': num_correct,
        }
        response = requests.post(
            api_endpoint, json=jsondata)
        if response.status_code == 200:
            st.success("Quiz submitted successfully!")
        else:
            st.error(f"Error submitting quiz: {response.text}")
    except Exception as e:
        st.error(f"Error submitting quiz: {str(e)}")


def app():
    # placeholder = st.empty()

    # with placeholder.container():
    if not st.session_state.started:
        num_mcqs = st.number_input(
            "Enter the number of MCQs", min_value=1, max_value=100, value=10, step=1)
        subject = st.selectbox("Select the subject", [
            "English", "Math", "Physics", "Intelligence", "Chemistry", "Computer", "Biology"])

        if st.button("Start Quiz"):
            st.session_state.started = True
            st.session_state.mcq_list = fetch_mcqs(num_mcqs, subject)

            create_quiz(num_mcqs, subject)

    if st.session_state.started and st.session_state.mcq_list:
        # Initialize answer array
        user_answers = []

        # Streamlit app
        st.title("MCQ Quiz Application")

        # Iterate through MCQs
        for i, mcq in enumerate(st.session_state.mcq_list):
            st.header(f"Question {i + 1}")
            st.write(mcq['mcqTitle'])

            # Display options
            options = [mcq['opt1'], mcq['opt2'], mcq['opt3'], mcq['opt4']]
            selected_option = st.radio(
                "Select your answer:", options, key=str(i))

            # Store user's answer
            user_answers.append(str(options.index(selected_option) + 1))

        # Submit button
        if st.button("Submit"):
            st.title("Quiz Submitted")
            st.write("Your Answers:", ', '.join(user_answers))

            # find the number of correct answers by comparing user_answers and mcq_list
            num_correct = 0
            for i, mcq in enumerate(st.session_state.mcq_list):
                if mcq['solution'] == user_answers[i]:
                    num_correct += 1

            st.write(f"Number of correct answers: {num_correct}")
            st.session_state.quizCorrectAnswers = num_correct

            # Uncomment the line below if you want to submit the quiz after displaying answers
            submit_quiz(num_correct)

    # placeholder.empty()
