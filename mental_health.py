# Import necessary libraries
import streamlit as st  # For creating a web-based application
import ollama  # For interacting with the AI language model
import base64  # For encoding images to Base64 for embedding

# Function to encode an image as a Base64 string
def get_base64(background):
    """
    Converts an image file to a Base64 encoded string.
    

    Args:
        background (str): Path to the image file.

    Returns:
        str: Base64 encoded string representation of the image.
    """
    with open(background, "rb") as image_file:
        data = image_file.read()
        return base64.b64encode(data).decode()

# Encode the background image
bin_str = get_base64("background.jpg")

# Apply custom background styling to the Streamlit app
st.markdown(
    f"""
    <style>
    .main{{
        background-image: url('data:image/jpg;base64,{bin_str}');
        background-style: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for conversation history
st.session_state.setdefault('conversation_history', [])

# Function to generate a response from the AI model
def generate_response(user_input):
    """
    Sends the user's message to the AI model and returns a response.

    Args:
        user_input (str): The user's input text.

    Returns:
        str: The AI-generated response.
    """
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})  # Record user input

    try:
        # Send conversation history to the AI model for a response
        response = ollama.chat(model="llama3.1:8b", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']  # Extract AI response
    except Exception as e:
        # Handle API errors gracefully
        ai_response = f"Oops! An error occurred while connecting to the chat service. Please try again later. (Error: {str(e)})"

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})  # Record AI response
    return ai_response

# Function to generate a positive affirmation
def generate_affirmation():
    """
    Generates a positive affirmation to encourage users.

    Returns:
        str: A positive affirmation.
    """
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to generate a short meditation guide
def generate_meditation_guide():
    """
    Generates a brief meditation guide to help users relax.

    Returns:
        str: A meditation guide.
    """
    prompt = "Provide a short meditation guide to help someone relax and reduce stress."
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Display the app title
st.title("Mental Health Support Agent")

# Display the chat history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"  # Identify message sender
    st.markdown(f"**{role}:** {msg['content']}")  # Display message

# Input field for user messages
user_message = st.text_input("How can I help you today?")

if user_message:
    # Generate and display the AI's response
    with st.spinner("Generating response..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Layout for the additional functionalities: Affirmations and Meditation Guide
col1, col2 = st.columns(2)  # Create two columns

with col1:
    if st.button("Give me a positive affirmation"):
        # Generate and display a positive affirmation
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a meditation guide"):
        # Generate and display a meditation guide
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Meditation Guide:** {meditation_guide}")
