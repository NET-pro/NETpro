import streamlit as stl
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv


def create_quiz_prompt_template():
    template= """
You are a teacher who is an excellent quiz maker. Your job is to create a quiz which only has Multiple Choice Questions. 
Each quiz has {num_questions} questions based on the given context {context} . 
You need to create all the questions relevant to the context, and make sure no question is repeated. 
Each question has four possible options. 
At the end of the quiz give all the answers together.
Only generate {num_questions} number of questions.
You generate text based mcqs on your own, and do not give me a python script to run. You have to generate the quiz and only respond with the questions, nothing else.

"""
    prompt = PromptTemplate(
        input_variables= ["num_questions", "context"],
        template= template

    )
    

    return prompt

def create_quiz_chain(prompt,llm):
    return LLMChain(llm = llm, prompt = prompt)
    
    

def app():
    load_dotenv()
    

    stl.write("Generate a context based quiz.")
    prompt = create_quiz_prompt_template()
    
    repo_id = "tiiuae/falcon-7b-instruct"
    llm = HuggingFaceHub(
        repo_id = repo_id, model_kwargs={})
    
    chain = create_quiz_chain(prompt, llm)
    context = stl.text_area("Enter the context")
    num_questions = stl.number_input("Enter the number of questions",min_value=1, max_value=100)
    if stl.button("Generate quiz"):
        quiz_response = chain.run(num_questions=num_questions, context=context)
        stl.write(quiz_response)
