import streamlit as st
import requests
st.session_state.started = False
st.session_state.quizComplete = False
st.session_state.mcqloop = False
st.session_state.num = 0

if 'num' not in st.session_state:
    st.session_state.num = 0


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
            print()
            return None
    except Exception as e:
        st.error(f"Error fetching MCQs: {str(e)}")
        print("wehru8i9weruifwheruif")
        return None


def submit_quiz(user_responses, subject):
    api_endpoint = "http://localhost:5000/quiz/user_attempted_quiz"

    try:
        response = requests.post(
            api_endpoint, json={"user_responses": user_responses, "subject": subject})
        if response.status_code == 200:
            st.success("Quiz submitted successfully!")
        else:
            st.error(f"Error submitting quiz: {response.text}")
    except Exception as e:
        st.error(f"Error submitting quiz: {str(e)}")


mcq_list = fetch_mcqs(10, "Math")


def app():

    # Initialize answer array
    user_answers = []

    # Streamlit app
    st.title("MCQ Quiz Application")

    # Iterate through MCQs
    for i, mcq in enumerate(mcq_list):
        st.header(f"Question {i + 1}")
        st.write(mcq['mcqTitle'])

        # Display options
        options = [mcq['opt1'], mcq['opt2'], mcq['opt3'], mcq['opt4']]
        selected_option = st.radio("Select your answer:", options, key=str(i))

        # Store user's answer
        user_answers.append(str(options.index(selected_option) + 1))

    # Submit button
    if st.button("Submit"):
        st.title("Quiz Submitted")
        st.write("Your Answers:", ', '.join(user_answers))
