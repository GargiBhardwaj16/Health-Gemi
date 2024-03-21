from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question , prompt):
    response = chat.send_message([prompt , question] , stream=True)
    return response

## define your prompt
prompt = """ You are a healthcare assistant. You are helping a patient with their mental health concerns. The patient says: He is lonely or sad. You need to cheer him/her up. By providing some motivational quotes or some jokes or songs. """

# Streamlit app configuration
st.set_page_config(page_title="PERSONAL HEALTHCARE ASSISTANT BOT", page_icon="🔮", layout="wide")

st.markdown("""
<style>
body {  /* Target the entire body for global background */
   background-color: yellow;
}

#chat-history {  /* Target a specific container with ID */
  background-color: lightblue;
  padding: 10px;
}
h1 {
  color: green;
  text-align: center;
}
</style>

<h1>Personal Healthcare Assistant</h1>
""", unsafe_allow_html=True)


st.header("Gemino : ")
# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Text input and submit button
input = st.text_input("How are you feeling? :", key="input")
submit = st.button("Submit")

# Handle user input and display response
if submit and input: 
    response = get_gemini_response(input, prompt)  # Pass the prompt here
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Gemino Bot:", chunk.text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

