import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Initialize the Groq client
# The client automatically looks for the GROQ_API_KEY environment variable
try:
    client = Groq()
except Exception as e:
    print("Error initializing client. Please ensure your .env file contains a valid GROQ_API_KEY.")
    exit(1)

def ask_groq(prompt, model_name="llama-3.3-70b-versatile"):
    """
    Sends a prompt to the Groq API and returns the response.
    """
    try:
        print(f"Sending request to {model_name}...\n")
        
        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, concise assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model_name,
            temperature=0.5,
            max_tokens=1024,
        )
        
        # Extract and return the text response
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"An API error occurred: {e}"

if __name__ == "__main__":
    # The question you want to ask
    user_prompt = "Explain quantum computing in Detail."
    
    print(f"User: {user_prompt}\n")
    
    # Call the function
    response = ask_groq(user_prompt)
    
    print("-" * 40)
    print(f"Groq:\n{response}")