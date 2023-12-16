import streamlit as stl
import mysql.connector
from chunking import get_pdf_text, get_text_chunks, get_vectorstore
from loginpage import register_user, authenticate_user



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
            
        else:
            stl.error("Invalid credentials")

def signup():
    stl.header("Sign Up")
    new_username = stl.text_input("Username")
    new_password = stl.text_input("Password", type="password")
    signup_button = stl.button("Sign Up")

    if signup_button:
        register_user(new_username, new_password)
        stl.success("Account created! Please log in.")

def app():
        stl.subheader("Your Documents")
        pdf_docs =  stl.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files = True)
        if stl.button("Process"):
            with stl.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the chunks
                text_chunks = get_text_chunks(raw_text)

                # store chunks in vector store
                vectorstore = get_vectorstore(text_chunks)
        