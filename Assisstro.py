import requests
import gradio as gr
import os
import streamlit as st

API_KEY = st.secrets["api_keys"]["API_KEY"]
API_URL = st.secrets["api_keys"]["API_URL"]

his = []
def perplexity_chatbot(query,history):
    messages = [{"role": "user", "content": "Act like a assistant. Reply in consise and minimum words."+query}]
    his.append( messages[0])
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar",  #sonar-pro
        "messages":his ,
        # "max_tokens": 150,
        # "temperature": 0.2
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        his.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    else:
        return f"Error: {response.status_code} - {response.text}"
offer = gr.ChatInterface(
    fn = perplexity_chatbot,
    type="messages"
)
port = int(os.environ.get("PORT", 7861))  #dynamic port 
offer.launch(server_name="0.0.0.0", server_port=port, share=False)


