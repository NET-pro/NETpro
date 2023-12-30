import streamlit as stl
from chunking import get_pdf_text, get_text_chunks, get_vectorstore
import requests


def authenticate_user(username, password):
    flask_api_url = 'http://localhost:5000/admin/login'

    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(flask_api_url, json=data)

        if response.status_code == 200:
            print("Login successful", response.json().get('uuid'))
            uuid = response.json().get('uuid')
            stl.session_state.uuid = uuid
            return True
        else:
            print(f"Login failed: {response.status_code}, {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")


def login():
    stl.header("Login")
    username = stl.text_input("Username")
    password = stl.text_input("Password", type="password")
    login_button = stl.button("Login")

    if login_button:
        if authenticate_user(username, password):
            stl.success("Login successful!")
            stl.session_state.is_authenticated = True
            stl.session_state.page = "main"
            stl.session_state.admin = True

        else:
            stl.error("Invalid credentials")

# def signup():
#     stl.header("Sign Up")
#     new_username = stl.text_input("Username")
#     new_password = stl.text_input("Password", type="password")
#     signup_button = stl.button("Sign Up")

#     if signup_button:
#         register_user(new_username, new_password)
#         stl.success("Account created! Please log in.")


def app():
    if stl.session_state.admin == True:

        stl.subheader("Your Documents")
        pdf_docs = stl.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if stl.button("Process"):
            with stl.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the chunks
                text_chunks = get_text_chunks(raw_text)

                # store chunks in vector store
                vectorstore = get_vectorstore(text_chunks)

        stl.subheader("Manage MCQs")

        # Add MCQ form
        stl.write("Add MCQ:")
        mcq_subject = stl.selectbox("MCQ Subject:", [
                                    "Math", "Chemistry", "Intelligence", "English", "Physics", "Computer", "Biology"])
        mcq_title = stl.text_input("MCQ Title:")
        opt1 = stl.text_input("Option 1:")
        opt2 = stl.text_input("Option 2:")
        opt3 = stl.text_input("Option 3:")
        opt4 = stl.text_input("Option 4:")
        solution = stl.text_input("Correct Solution:")

        if stl.button("Submit MCQ"):
            # Validate and insert the MCQ into the database
            if mcq_subject and mcq_title and opt1 and opt2 and opt3 and opt4 and solution:
                try:
                    # Prepare data for API request
                    mcq_data = {
                        "uuid": stl.session_state.uuid,  # Replace with actual admin user UUID
                        "mcqSubject": mcq_subject,
                        "mcqTitle": mcq_title,
                        "opt1": opt1,
                        "opt2": opt2,
                        "opt3": opt3,
                        "opt4": opt4,
                        "solution": solution
                    }

                    # Make API request to add MCQ
                    response = requests.post(
                        "http://localhost:5000/mcq/add_mcq", json=mcq_data)

                    if response.status_code == 200:
                        stl.success("MCQ submitted successfully.")
                    else:
                        stl.error(f"Error submitting MCQ: {response.text}")
                except Exception as e:
                    stl.error(f"Error submitting MCQ: {str(e)}")
            else:
                stl.warning("Please fill in all fields before submitting.")

    else:
        stl.subheader("You are not admin.")
