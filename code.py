from google.cloud import aiplatform
import os

# Initialize the AI Platform client
def initialize_ai_client():
    """
    Initialize the Google AI client using service account credentials.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-service-account-key.json"  # Update with the path
    aiplatform.init(
        project="your-gcp-project-id",  # Replace with your GCP project ID
        location="us-central1"          # Replace with your region
    )

# Generate a response using the Gemini II model
def generate_response(user_input):
    """
    Sends a user query to the Gemini II model and returns the response.
    """
    try:
        # Define the model path
        model_path = (
            "projects/your-gcp-project-id/locations/us-central1/"
            "publishers/google/models/text-bison@001"  # Replace with the correct model name if different
        )
        
        # Load the model
        model = aiplatform.Model(model_path)
        
        # Make the prediction
        prediction = model.predict(
            instances=[{"content": user_input}],
            parameters={
                "temperature": 0.7,       # Adjust creativity
                "maxOutputTokens": 200    # Adjust length of response
            }
        )
        
        # Extract and return the response
        return prediction.predictions[0]["content"].strip()
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
    initialize_ai_client()
    chatbot()
