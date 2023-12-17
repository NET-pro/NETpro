import streamlit as st
import mysql.connector

# Connect to MySQL database


def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="langchain"
    )
    return conn

# Function to initialize the database and insert sample MCQs


def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Create MCQ table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mcqs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            correct_option TEXT
        )
    """)

    # Insert sample MCQs if the table is empty
    cursor.execute("SELECT COUNT(*) FROM mcqs")
    if cursor.fetchone()[0] == 0:
        sample_mcqs = [
            ("What is the capital of France?", "Paris",
             "Berlin", "Madrid", "Rome", "Paris"),
            ("Which planet is known as the Red Planet?",
             "Earth", "Mars", "Jupiter", "Saturn", "Mars"),
            # Add more sample MCQs as needed
        ]
        cursor.executemany("""
            INSERT INTO mcqs (question, option1, option2, option3, option4, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, sample_mcqs)

    conn.commit()
    conn.close()


def authenticate_user_quiz(password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE password=%s", (password,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


# Function to fetch MCQs from the database
def fetch_mcqs():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mcqs")
    mcqs = cursor.fetchall()
    conn.close()
    return mcqs

# Streamlit app


def app():
    st.title("NET Simulation")

    # Initialize the database and insert sample MCQs
    initialize_database()

    st.write("Enter the password to generate MCQs:")
    password = st.text_input("Passwords", type="password")
    generatequiz = st.button("Generate")
    if generatequiz:
        if authenticate_user_quiz(password):
            st.success("Password correct! MCQs are ready to be generated.")
            mcqs = fetch_mcqs()

            # Display MCQs
            for mcq in mcqs:
                st.write(f"**Q: {mcq['question']}**")
                options = [mcq['option1'], mcq['option2'],
                           mcq['option3'], mcq['option4']]
                selected_option = st.radio("Select an option:", options)

        elif password == "":
            st.error("Please Enter password")

        else:
            st.error("Incorrect password. Please try again")
