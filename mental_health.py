import os
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_groq import ChatGroq
from IPython.display import display
import gradio as gr
import random

# Define the state of the mental health chatbot
class MentalHealthState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "Messages in the conversation"]
    current_feelings: str
    struggles: List[str]
    support_suggestions: str

# Initialize Groq model for generating responses
llm = ChatGroq(
    temperature=0.7,  # Increase randomness for varied outputs
    groq_api_key="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",
    model_name="llama-3.3-70b-versatile"
)

# Therapist-style prompt variations to ensure diverse and supportive responses
PROMPT_VARIATIONS = [
    "You are a compassionate therapist helping someone through a tough time. Listen closely to their feelings, validate their emotions, and provide thoughtful advice. Be caring and warm.",
    "You are a licensed therapist offering empathetic and personalized support to a user sharing their struggles. Offer practical steps and ensure they feel heard.",
    "You are an experienced counselor specializing in mental health. Always focus on reassurance, empathy, and actionable strategies to help the user navigate their challenges."
]

# Generate a dynamic prompt template
def generate_prompt_template():
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", random.choice(PROMPT_VARIATIONS)),
        ("human", "I am feeling {current_feelings} and I am struggling with {struggles}. Can you help me?")
    ])
    return prompt_template

# Functions for updating user state based on feelings and struggles

def input_feelings(feelings: str, state: MentalHealthState) -> MentalHealthState:
    """
    Updates the state with the user's feelings.
    """
    return {
        **state,
        "current_feelings": feelings,
        "messages": state['messages'] + [HumanMessage(content=f"I am feeling {feelings}.")],
    }

def input_struggles(struggles: str, state: MentalHealthState) -> MentalHealthState:
    """
    Updates the state with the user's struggles.
    """
    return {
        **state,
        "struggles": struggles.split(", "),
        "messages": state['messages'] + [HumanMessage(content=f"I am struggling with: {struggles}.")],
    }

# Function to generate a supportive response and suggest coping mechanisms
def provide_support(state: MentalHealthState) -> str:
    """
    Generates a response to provide emotional support and coping strategies.
    """
    # Get a dynamically generated prompt template
    mental_health_prompt = generate_prompt_template()

    # Get the assistant's response from the Groq model
    response = llm.invoke(mental_health_prompt.format_messages(
        current_feelings=state['current_feelings'],
        struggles=", ".join(state['struggles'])
    ))

    # Add varied encouraging phrases
    encouragement_phrases = [
        "You're not alone, and this is a safe space for you to share.",
        "It's okay to feel this way—you're taking an important step by reaching out.",
        "Every small step forward counts, and I'm here to support you.",
        "You have the strength to overcome this, even if it doesn't feel that way now.",
    ]

    # Personalizing the response with more encouragement
    suggestions = response.content
    return f"{suggestions}\n\n{random.choice(encouragement_phrases)}"

# Main function to handle the mental health chatbot conversation
def mental_health_chat(feelings: str, struggles: str) -> str:
    """
    Main function that handles the conversation and updates the state.
    """
    state: MentalHealthState = {
        "messages": [],
        "current_feelings": "",
        "struggles": [],
        "support_suggestions": "",
    }

    state = input_feelings(feelings, state)
    state = input_struggles(struggles, state)

    support_response = provide_support(state)

    return support_response

# Gradio Interface for interacting with the chatbot
interface = gr.Interface(
    fn=mental_health_chat,
    inputs=[
        gr.Textbox(label="How are you feeling?"),
        gr.Textbox(label="What are you struggling with? (comma-separated)"),
    ],
    outputs=gr.Textbox(label="Support and Suggestions"),
    title="Therapist-Style Mental Health Chatbot",
    description="Talk to this chatbot about your feelings and struggles. It will provide emotional support and suggest helpful coping strategies tailored to you."
)

# Launch the chatbot interface
interface.launch(share=False)
