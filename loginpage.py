# loginpage.py
# loginpage.py
import streamlit as stl
import requests


def register_user(username, password, email):
    flask_api_url = 'http://localhost:5000/user/register'
    data = {
        'username': username,
        'password': password,
        'email': email
    }
    response = requests.post(flask_api_url, json=data)

    try:
        if response.status_code == 200:
            print("User registered successfully")
        else:
            print(f"Error: {response.status_code}, {response.json()}")
    except requests.RequestException as e:
        print(f"Error: {e}")


def authenticate_user(username, password):
    flask_api_url = 'http://localhost:5000/user/login'
    # Replace with the username and password you want to use for login
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
            return "Login successful"
        else:
            print(f"Login failed: {response.status_code}, {response.json()}")
            return "Login failed"
    except requests.RequestException as e:
        print(f"Error: {e}")


def login():
    stl.header("Login")
    username = stl.text_input("Username")
    password = stl.text_input("Password", type="password")
    login_button = stl.button("Login")

    if login_button:
        if "Login failed" not in authenticate_user(username, password):
            stl.success("Login successful!")
            stl.session_state.is_authenticated = True
            stl.session_state.page = "main"

        else:
            stl.error("Invalid credentials")


def signup():
    stl.header("Sign Up")
    new_username = stl.text_input("Username")
    new_password = stl.text_input("Password", type="password")
    email = stl.text_input("Email")
    signup_button = stl.button("Sign Up")

    if signup_button and new_username and new_password and email:
        register_user(new_username, new_password, email)
        stl.success("Account created! Please log in.")
