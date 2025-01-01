import streamlit as st
import ollama 
import base64


def get_base64(background):
    with open(background, "rb") as image_file:
        data = image_file.read()
        return base64.b64encode(data).decode()


bin_str = get_base64("background.jpg")

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


st.session_state.setdefault('conversation_history', [])


def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model="llama3.1:8b", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
    except Exception as e:
        ai_response = f"Oops! An error occurred while connecting to the chat service. Please try again later. (Error: {str(e)})"

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response


def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelming ?"
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


def generate_meditation_guide():
    prompt = "Provide a short meditation guide to help someone relax and reduce stress"
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


st.title("Mental Health Support Agent")

for msg in st.session_state['conversation_history']:
    role = "you" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:**{msg['content']}")

user_message = st.text_input("How can I help You today ?")

if user_message:
    with st.spinner("Generating response..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:**{ai_response}")

col1, col2 = st.columns(2)

with col1:
    if st.button("give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:**{affirmation}")

with col2:
    if st.button(" give me a meditation guide"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Meditation Guide:**{meditation_guide}")
