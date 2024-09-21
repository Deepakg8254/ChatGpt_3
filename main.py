import openai
import os
import streamlit as st

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is set as an environment variable

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

# Streamlit app
def main():
    st.title("GPT-4 Enhanced Chatbot")

    # Display the conversation history
    st.write("### Chat History")
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**GPT-4:** {message['content']}")

    # Input box for the user to continue conversation
    st.text_input("Type your message here:", key="user_input", on_change=handle_conversation)

    # Button to clear chat history
    if st.button("Clear Chat"):
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Optional: Adding sidebar for additional controls
    st.sidebar.title("Settings")
    st.sidebar.slider("Max Tokens", min_value=500, max_value=3000, value=1500, step=100, help="Adjust the length of the GPT-4 response")
    st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="Adjust the creativity of GPT-4's responses")

if __name__ == "__main__":
    main()
