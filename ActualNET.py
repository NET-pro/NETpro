import streamlit as st
import requests


def fetch_mcqs(num_mcqs, subject):
    api_endpoint = "http://localhost:5000/mcq/get_mcqs?num_mcqs=5&subject=Math"
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


def app():
    st.title("NET Simulation")

    # Input for the number of MCQs
    num_mcqs = st.number_input(
        "Enter the number of MCQs", min_value=1, value=5)

    # Dropdown for subjects
    subjects = ["Math", "Chemistry", "Intelligence",
                "English", "Physics", "Computer", "Biology"]
    selected_subject = st.selectbox("Select a Subject", subjects)

    # Fetch MCQs from the backend
    fetched_mcqs = fetch_mcqs(num_mcqs, selected_subject)

    # Display MCQs and collect user responses
    user_responses = {}
    if fetched_mcqs:
        st.subheader(f"Quiz: {selected_subject}")
        for idx, mcq in enumerate(fetched_mcqs, start=1):
            st.write(f"{idx}. {mcq['mcqTitle']}")

            # Options
            options = [mcq['opt1'], mcq['opt2'], mcq['opt3'], mcq['opt4']]
            selected_options = st.checkbox(
                f"Select options for Question {idx}:", options, key=f"q_{mcq['mcqID']}_{idx}")

            # Store user response
            user_responses[f"q_{mcq['mcqID']}_{idx}"] = selected_options

            st.markdown("---")

        # Button to submit quiz
        if st.button("Submit Quiz"):
            # Print user responses
            st.subheader("User Responses:")
            for key, selected_options in user_responses.items():
                if key.startswith("q_"):
                    st.write(f"{key}: {selected_options}")
