from google.cloud import aiplatform

# Initialize the API client
def initialize_ai_client(api_key):
    """
    Initialize the Google AI client using the provided API key.
    """
    aiplatform.init(
        project="your-gcp-project-id",  # Replace with your Google Cloud project ID
        location="us-central1"          # Replace with your region if needed
    )
    # Set the API key as an environment variable
    import os
    os.environ["GOOGLE_API_KEY"] = AIzaSyBjG0fvTKF-_urlOO9Llv59Qlm2U1hn0kA

# Generate a response using Gemini II
def generate_response(user_input, api_key):
    """
    Sends a user query to the Gemini II model via the PaLM API and returns the response.
    """
    try:
        # Set the Gemini endpoint and initialize the client
        endpoint = "text-bison@001"  # Replace with the Gemini II model endpoint if different
        client = aiplatform.gapic.PredictionServiceClient()
        
        # Define model path
        project_id = "glass-arcade-444305-u5"  # Replace with your Google Cloud Project ID
        location = "us-central1"           # Replace with your region
        model_path = f"projects/{project_id}/locations/{location}/publishers/google/models/{endpoint}"
        
        # Send the user input to the model
        response = client.predict(
            endpoint=model_path,
            instances=[{"content": user_input}],
            parameters={
                "temperature": 0.7,       # Adjust creativity
                "maxOutputTokens": 200   # Adjust length of response
            },
            api_key=api_key  # Pass the API key directly
        )
        
        # Extract and return the response
        prediction = response.predictions[0]["content"]
        return prediction.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Main chatbot loop
def chatbot(api_key):
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
        response = generate_response(user_input, api_key)
        print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    API_KEY = "your_gemini_api_key"  # Replace with your Gemini API key
    initialize_ai_client(API_KEY)
    chatbot(API_KEY)

