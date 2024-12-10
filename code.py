import openai
import streamlit as st
# Debugging step: Print out available secrets
st.write("Available secrets:", list(st.secrets.keys()))

# Try setting the API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# API Key Configuration
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define a function to interact with GPT
def generate_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate and supportive mental health assistant. Provide helpful advice, mindfulness techniques, and resources for professional help."},
                {"role": "user", "content": user_input},
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit App
st.title("AI-Powered Mental Health Chatbot")
st.markdown("""
This chatbot provides basic mental health support. It can suggest mindfulness activities, calming techniques, and point you towards professional resources if needed.  
**Disclaimer**: This is not a replacement for professional mental health care.
""")

# Input from User
user_input = st.text_area("How can I help you today?", height=150)

if st.button("Submit"):
    if user_input:
        with st.spinner("Thinking..."):
            response = generate_response(user_input)
        st.markdown("### Response:")
        st.write(response)
    else:
        st.warning("Please enter your message.")

# Optional: Provide emergency resources
st.markdown("""
---
If you are in crisis, please reach out to a professional:  
- [National Suicide Prevention Lifeline (US)](https://suicidepreventionlifeline.org)  
- Call 911 (US) or your country's emergency services.  
""")
