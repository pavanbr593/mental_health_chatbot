import os
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import random
import streamlit as st

# Define the state of the mental health chatbot
class MentalHealthState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "Messages in the conversation"]
    current_feelings: str
    struggles: List[str]
    support_suggestions: str

# Initialize Groq model for generating responses
llm = ChatGroq(
    temperature=0.7,  # Adjusted for diverse outputs
    groq_api_key="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",
    model_name="llama-3.3-70b-versatile"
)

# Randomized supportive closing messages
closing_messages = [
    "Remember, you're stronger than you think, and it's okay to take things one step at a time.",
    "You're not alone in this journey—small steps lead to big changes.",
    "It's perfectly okay to feel this way; tomorrow is a fresh start.",
    "You are valued and capable, even on the toughest days. Keep going!",
    "Every challenge you face is a step toward growth. You’ve got this!"
]

# Chat prompt template for empathy and understanding
mental_health_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a caring and empathetic mental health assistant. When a user shares their feelings, always respond with understanding and compassion. Offer emotional support and helpful, practical coping strategies. Show the user they are not alone, and provide reassurance that it is okay to have difficult feelings. Avoid being overly clinical—create a warm and safe environment for them."),
    ("human", "I am feeling {current_feelings} and I am struggling with {struggles}. Can you help me?"),
])

# Functions for updating user state based on feelings and struggles

def input_feelings(feelings: str, state: MentalHealthState) -> MentalHealthState:
    return {
        **state,
        "current_feelings": feelings,
        "messages": state['messages'] + [HumanMessage(content=f"I am feeling {feelings}.")],
    }

def input_struggles(struggles: str, state: MentalHealthState) -> MentalHealthState:
    return {
        **state,
        "struggles": struggles.split(", "),
        "messages": state['messages'] + [HumanMessage(content=f"I am struggling with: {struggles}.")],
    }

# Function to generate a supportive response and suggest coping mechanisms
def provide_support(state: MentalHealthState) -> str:
    response = llm.invoke(mental_health_prompt.format_messages(
        current_feelings=state['current_feelings'],
        struggles=", ".join(state['struggles'])
    ))

    closing_message = random.choice(closing_messages)
    suggestions = response.content

    return f"{suggestions}\n\n{closing_message}"

# Streamlit App
def main():
    st.title("Mental Health Support Chatbot")
    st.write("Talk to this chatbot about your feelings and struggles. It will provide emotional support and suggest helpful coping strategies. You're not alone.")

    # User inputs
    feelings = st.text_input("How are you feeling?", placeholder="e.g., anxious, stressed")
    struggles = st.text_area("What are you struggling with? (comma-separated)", placeholder="e.g., work pressure, relationships")

    if st.button("Get Support"):
        if feelings and struggles:
            state: MentalHealthState = {
                "messages": [],
                "current_feelings": "",
                "struggles": [],
                "support_suggestions": "",
            }

            state = input_feelings(feelings, state)
            state = input_struggles(struggles, state)

            # Generate support response
            support_response = provide_support(state)

            # Display the response
            st.markdown(f"### Support and Suggestions\n{support_response}")
        else:
            st.warning("Please fill in both fields to receive support.")

if __name__ == "__main__":
    main()
