#The Logic of conversing for AskDoubt
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from HTMLTemplates import css, user_template, bot_template
import streamlit as stl

from Llamacall import llm





def get_conversation_chain (vectorstore):


    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput (user_question):
    response = stl.session_state.conversation({'question': user_question})
    stl.session_state.chat_history = response['chat_history']

    for i,message in enumerate(stl.session_state.chat_history):
        if i% 2 ==0:
            stl.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            stl.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)