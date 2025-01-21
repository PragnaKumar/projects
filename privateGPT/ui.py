import streamlit as st
import random
import time
import requests
import os

# confugurations
url = 'http://0.0.0.0:8506/prompt'
title_of_app ="PrivateGPT"

def run_gpt_query(query):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        'data': query,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
   
st.title(title_of_app)

uploadfile = st.sidebar.file_uploader("Upload your file", type=("pdf"))

upload_dir = r"/mnt/d/llm/privateGPT/source_documents" #add the path of the source_documents path here

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

st.success("File uploaded successfully!")

if uploadfile is not None:

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Run SQL query with loading spinner
        with st.spinner("Processing..."):
            query_result = run_gpt_query(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.write("Query Result:") 
            # Display the query result after processing
            st.write(query_result)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": query_result})

else:
    st.warning('Please upload your file!')