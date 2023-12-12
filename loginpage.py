# loginpage.py
# loginpage.py
import streamlit as stl
import mysql.connector

def create_connection():
    conn= mysql.connector.connect(
        host="localhost",
        username= "root",
        password= "Lostinsonder4",
        database= "langchain"
    )
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)""")
    conn.commit()
    conn.close()

def register_user(username, password):
    conn= create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    conn= create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None



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
