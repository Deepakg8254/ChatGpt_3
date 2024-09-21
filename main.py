import openai
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Set up your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Ensure your API key is set as an environment variable

# Initialize session state to store the conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]  # Initial system message to set GPT-4 behavior

# Function to get a response from GPT-4
def ask_gpt4(messages):
    response = openai.ChatCompletion.create(  # Correct method name
        model="gpt-4",
        messages=messages,
        max_tokens=1500,  # Adjust as needed
        temperature=0.7,  # Adjust creativity level
    )
    return response['choices'][0]['message']['content']

# Function to handle user input and model response
def handle_conversation():
    user_input = st.session_state.user_input  # Capture the user input from the session state

    if user_input:
        # Add user message to the conversation history
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Get GPT-4's response
        with st.spinner("GPT-4 is thinking..."):
            response = ask_gpt4(st.session_state["messages"])

        # Add GPT-4's response to the conversation history
        st.session_state["messages"].append({"role": "assistant", "content": response})

        # Clear input after response
        st.session_state.user_input = ""

# Function to download the chat history
def download_chat_history():
    messages = st.session_state["messages"]
    chat_data = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    df = pd.DataFrame(chat_data)
    return df.to_csv(index=False)

# Function to format chat messages
def format_message(role, content):
    if role == "user":
        st.markdown(f'<div style="background-color: #5d6d7e; padding: 10px; border-radius: 10px;"><strong>You:</strong> {content}</div>', unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f'<div style="background-color: #283747; padding: 10px; border-radius: 10px;"><strong>GPT-4:</strong> {content}</div>', unsafe_allow_html=True)

# Main Streamlit app function
def main():
    st.title("GPT-4 Enhanced Chatbot")

    # Display the conversation history
    st.write("### Chat")
    chat_placeholder = st.empty()
    with chat_placeholder.container():
        for message in st.session_state["messages"]:
            format_message(message["role"], message["content"])

    # Auto-scroll to the latest message
    components.html("<script>window.scrollTo(0, document.body.scrollHeight);</script>")

    # Input box for the user to continue conversation
    st.text_input("Type your message here:", key="user_input", on_change=handle_conversation)

    # Button to clear chat history
    if st.button("Clear Chat"):
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Sidebar settings for token and temperature adjustments
    st.sidebar.title("Settings")
    st.sidebar.slider("Max Tokens", min_value=500, max_value=3000, value=1500, step=100, help="Adjust the length of the GPT-4 response")
    st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="Adjust the creativity of GPT-4's responses")

    # Download chat history button
    if st.sidebar.button("Download Chat History"):
        csv = download_chat_history()
        st.sidebar.download_button(
            label="Download Chat as CSV",
            data=csv,
            file_name='chat_history.csv',
            mime='text/csv',
        )

    # Warning if input is too long
    if len(st.session_state.get('user_input', '')) > 1000:
        st.warning("Your input is too long, consider shortening it.")

if __name__ == "__main__":
    main()
