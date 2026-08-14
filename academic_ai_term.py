import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Initialize the Groq client
try:
    client = Groq()
except Exception as e:
    print("Error initializing client. Please ensure your .env file contains a valid GROQ_API_KEY.")
    exit(1)

def ask_groq_academic(prompt, model_name="llama-3.3-70b-versatile"):
    """
    Sends a prompt to the Groq API using an MSc Academic Expert persona.
    """
    
    # Define the Academic Persona
    system_persona = (
        "You are a distinguished academic expert and university professor. "
        "Your primary task is to provide answers that are highly rigorous, analytical, "
        "and structured appropriately for a Master of Science (MSc) end-semester examination. "
        "You must use formal academic language, incorporate relevant theoretical frameworks, "
        "empirical evidence, and scientific principles where applicable. Ensure your explanations "
        "are comprehensive, meticulously organized, and demonstrate profound subject-matter expertise."
    )

    try:
        print(f"Sending request to {model_name}...\n")
        
        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_persona
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model_name,
            # Lower temperature (e.g., 0.2 - 0.3) makes the output more focused and deterministic, 
            # which is ideal for factual, academic writing.
            temperature=0.3, 
            # Increased max tokens to accommodate longer, essay-style answers
            max_tokens=2048, 
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"An API error occurred: {e}"

if __name__ == "__main__":
    # A sample MSc-level examination question
    user_prompt = "Critically evaluate the principles of quantum entanglement and discuss its fundamental implications for quantum cryptographic protocols."
    
    print(f"User Question: {user_prompt}\n")
    
    # Call the function
    response = ask_groq_academic(user_prompt)
    
    print("-" * 60)
    print("Academic Expert Evaluation:\n")
    print(response)
    print("-" * 60)