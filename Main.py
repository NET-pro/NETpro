# main.py
import streamlit as stl
from streamlit_option_menu import option_menu
import loginpage
import overview, final, Quiz, ActualNET, SubjectiveNET
import Admin

def main():
    stl.set_page_config(page_title="NETPro", page_icon="books", layout= "centered")

    stl.header("NETPro :books:")

    loginpage.create_table()


    
    if 'is_authenticated' not in stl.session_state:
        stl.session_state.is_authenticated = False

    # Initialize session_state.page if it doesn't exist
    if 'page' not in stl.session_state:
        stl.session_state.page = "login"



    if not stl.session_state.is_authenticated:
        loginsign = stl.empty()
        with loginsign.container():


            #inserting admin button
            admin_col, user_col = stl.columns(2, gap = "small")
            with admin_col:
                admin = stl.checkbox("Admin")

            with user_col:
                user = stl.checkbox("User")

            #if admin chosen move to admin login
            if admin and not user:
                stl.write("Hello admin")
                login_or_signup = stl.radio("Choose an option", ("Login", "Sign Up"))

                if login_or_signup == "Login":
                    #Making a container to delete login stuff after loging in
                        loginpage.login()
                        if stl.session_state.is_authenticated:
                            Admin.stl.session_state.page = "admin"
                            loginsign.empty()

                elif login_or_signup == "Sign Up":
                    loginpage.signup()
                    if stl.session_state.is_authenticated:
                        stl.session_state.page = "main"

                
            #If user pressed
            if user and not admin:
                login_or_signup = stl.radio("Choose an option", ("Login", "Sign Up"))

                if login_or_signup == "Login":
                    #Making a container to delete login stuff after loging in
                        loginpage.login()
                        if stl.session_state.is_authenticated:
                            stl.session_state.page = "main"
                            loginsign.empty()

                elif login_or_signup == "Sign Up":
                    loginpage.signup()
                    if stl.session_state.is_authenticated:
                        stl.session_state.page = "main"
            
    if stl.session_state.page == "main":
        class MultiApp:
            def __init__(self):
                self.apps = []

            def add_app(self, title, function):
                self.apps.append({
                    "title": title,
                    "function": function
                })

            def run(self):
                with stl.sidebar:
                    app = option_menu(
                        menu_title='NETPro',
                        options=['Overview','ActualNET', 'SubjectiveNET', 'Dashboard', 'AskDoubt', 'Account'],
                        icons=[':page_with_curl:', 'house_fill', 'ok_hand', 'sleuth_or_spy',':page_with_curl:',':page_with_curl:'],
                        menu_icon='chat-text-fill',
                        default_index=1,
                        styles={
                            "container": {"padding": "5!important", "background-color": '#212B48'},
                            "icon": {"color": "white", "font-size": "25px"},
                            "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px"},
                            "nav-link-selected": {"background-color": "#17192F"},
                        }
                    )

                if app == 'Overview':
                    overview.app()
                if app == "AskDoubt":
                    final.app()
                if app == "Quiz":
                    Quiz.app()
                if app == "ActualNET":
                    ActualNET.app()
                if app == "SubjectiveNET":
                    SubjectiveNET.app()
                if app == "Account":
                    stl.write("Welcome to the Account Page")
                    logout_button = stl.button("Logout")
                    if logout_button:
                        stl.session_state.is_authenticated = False
                        

        app = MultiApp()
        app.run()
    


    #The pathway to the admin side
    if stl.session_state.page == "admin":
        Admin.app(


        )
if __name__ == "__main__":
    main()
             