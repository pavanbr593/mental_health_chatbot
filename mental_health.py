import os
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_groq import ChatGroq
from IPython.display import display
import gradio as gr

# Define the state of the mental health chatbot
class MentalHealthState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "Messages in the conversation"]
    current_feelings: str
    struggles: List[str]
    support_suggestions: str

# Initialize Groq model for generating responses
llm = ChatGroq(
    temperature=0,
    groq_api_key="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",
    model_name="llama-3.3-70b-versatile"
)

# Chat prompt template to enhance empathy and understanding in responses
mental_health_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a caring and empathetic mental health assistant. When a user shares their feelings, always respond with understanding and compassion. Offer emotional support and helpful, practical coping strategies. Show the user they are not alone, and provide reassurance that it is okay to have difficult feelings. Avoid being overly clinical—create a warm and safe environment for them."),
    ("human", "I am feeling {current_feelings} and I am struggling with {struggles}. Can you help me?"),
])

# Functions for updating user state based on feelings and struggles

def input_feelings(feelings: str, state: MentalHealthState) -> MentalHealthState:
    """
    Updates the state with the user's feelings.

    Args:
    feelings (str): The current feelings of the user.
    state (MentalHealthState): The current state of the chatbot.

    Returns:
    MentalHealthState: The updated state with the user's feelings.
    """
    return {
        **state,
        "current_feelings": feelings,
        "messages": state['messages'] + [HumanMessage(content=f"I am feeling {feelings}.")],
    }

def input_struggles(struggles: str, state: MentalHealthState) -> MentalHealthState:
    """
    Updates the state with the user's struggles.

    Args:
    struggles (str): The struggles of the user (comma-separated).
    state (MentalHealthState): The current state of the chatbot.

    Returns:
    MentalHealthState: The updated state with the user's struggles.
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

    Args:
    state (MentalHealthState): The current state of the chatbot, including feelings and struggles.

    Returns:
    str: The generated response containing suggestions and emotional support.
    """
    # Get the assistant's response from the Groq model
    response = llm.invoke(mental_health_prompt.format_messages(
        current_feelings=state['current_feelings'],
        struggles=", ".join(state['struggles'])
    ))

    # Personalizing the response with more encouragement
    suggestions = response.content
    return f"{suggestions}\n\nRemember, it's completely okay to feel this way. You're doing the best you can, and that matters. You're not alone in this, and I believe in you!"

# Main function to handle the mental health chatbot conversation
def mental_health_chat(feelings: str, struggles: str) -> str:
    """
    Main function that handles the conversation and updates the state.

    Args:
    feelings (str): The user's feelings.
    struggles (str): The user's struggles (comma-separated).

    Returns:
    str: The final response with emotional support and coping strategies.
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
    title="Mental Health Support Chatbot",
    description="Talk to this chatbot about your feelings and struggles. It will provide emotional support and suggest helpful coping strategies. You're not alone."
)

# Launch the chatbot interface
interface.launch(share=False)

