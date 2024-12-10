from google.cloud import aiplatform
import os

# Initialize the API client
def initialize_ai_client(api_key):
    """
    Initialize the Google AI client using the provided API key.
    """
    os.environ["GOOGLE_API_KEY"] = api_key
    aiplatform.init(
        project="your-gcp-project-id",  # Replace with your Google Cloud project ID
        location="us-central1"          # Replace with your region if needed
    )

# Generate a response using Gemini II
def generate_response(user_input):
    """
    Sends a user query to the Gemini II model via the PaLM API and returns the response.
    """
    try:
        # Define the model path
        project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
        location = "us-central1"           # Replace with your region
        model_name = "text-bison@001"      # Replace with the Gemini II model endpoint if different
        model_path = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}"
        
        # Make the prediction
        prediction = aiplatform.Model(model_path).predict(
            instances=[{"content": user_input}],
            parameters={
                "temperature": 0.7,       # Adjust creativity
                "maxOutputTokens": 200   # Adjust length of response
            }
        )
        
        # Extract and return the response
        response_content = prediction.predictions[0]["content"]
        return response_content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Main chatbot loop
def chatbot():
    """
    Main function to interact with the chatbot.
    """
    print("Welcome to the Gemini II-powered Chatbot!")
    print("Ask me anything. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! Take care.")
            break
        
        # Get the chatbot's response
        response = generate_response(user_input)
        print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    API_KEY = "your_gemini_api_key"  # Replace with your Gemini API key
    initialize_ai_client(API_KEY)
    chatbot()
