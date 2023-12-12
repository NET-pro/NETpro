#The AskDoubt where the graphic for AskDoubt is present
import streamlit as stl
from dotenv import load_dotenv
from HTMLTemplates import css, user_template, bot_template

from ConversationChain import get_conversation_chain, handle_userinput
from chunking import get_pdf_text, get_text_chunks, get_vectorstore


def app():
    load_dotenv()
   # stl.set_page_config(page_title="NETPro", page_icon="books")

#     stl.write(css, unsafe_allow_html=True)

#     if "conversation" not in stl.session_state:
#         stl.session_state.conversation = None

#     if "chat-history" not in stl.session_state:
#         stl.session_state.chat_history = None

    stl.header("Chat with multiple books :books:")
    user_question = stl.text_input("Ask a question:")
    if user_question:
        handle_userinput(user_question)

    with stl.sidebar:
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

                #conversing on the vectorstore
                stl.session_state.conversation = get_conversation_chain(vectorstore)


