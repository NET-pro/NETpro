import streamlit as stl
import SubjectiveNET, ActualNET

def app():

    placeholder = stl.empty()

    with placeholder.container():

        container_color = "#17192F"
        # Center the container using CSS styling
        stl.markdown(
        f"""
        <style>
            .custom-container {{
                max-width: {1000}px;
                margin-left: auto;
                margin-right: auto;
                margin-top: {1000}px;
                background-color: {container_color};
                padding: 20px;
                text-align: center;
            }}
        </style>
        """
        , unsafe_allow_html=True
    )

        # Your container content
        stl.title("Centered Container Example")

        # Insert your content within the centered container
        stl.text("This is some content inside the centered container.")

    if stl.button("Actual"):
            placeholder.empty()
            ActualNET.app()
            

    if stl.button("Subjective"):
            placeholder.empty()
            SubjectiveNET.app()
            