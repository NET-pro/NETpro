import json
import streamlit as stl
from streamlit_lottie import st_lottie


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def app():
    
    lottie_coding = load_lottiefile("Lottiefiles/coding.json")
    st_lottie(
        lottie_coding,
        loop= True,
        height= 700
    )
    
    
    
    stl.subheader("Overview ")
    