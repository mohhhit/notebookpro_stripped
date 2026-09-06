import os
import markdown
from xhtml2pdf import pisa
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment variables
load_dotenv()

# 2. Initialize Groq client
try:
    client = Groq()
except Exception as e:
    print("Error initializing client. Please ensure your .env file contains a valid GROQ_API_KEY.")
    exit(1)
modelname = "qwen/qwen3.8-27b"
def ask_groq_academic(prompt, model_name=modelname):
    system_persona = (
        "You are a distinguished academic expert and university professor. "
        "Your primary task is to provide answers that are highly rigorous, analytical, "
        "and structured appropriately for a Master of Science (MSc) end-semester examination. "
        "You must use formal academic language, incorporate relevant theoretical frameworks, "
        "empirical evidence, and scientific principles where applicable. Ensure your explanations "
        "are comprehensive, meticulously organized, and demonstrate profound subject-matter expertise."
    )

    try:
        print(f"\nSending request to {model_name}...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_persona},
                {"role": "user", "content": prompt}
            ],
            model=model_name,
            temperature=0.3, 
            max_tokens=2048, 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An API error occurred: {e}")
        return None

def save_markdown_to_pdf(markdown_text, output_filename):
    """Converts markdown text to HTML and saves it as a PDF using xhtml2pdf."""
    
    html_body = markdown.markdown(markdown_text, extensions=['extra'])
    
    html_content = f'''
    <html>
    <head>
        <style>
            @page {{
                size: a4;
                margin: 2cm;
            }}
            body {{
                font-family: Helvetica, Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.5;
                color: #222222;
            }}
            h1 {{
                font-size: 18pt;
                text-align: center;
                color: #800000;
                padding-bottom: 10px;
            }}
            h2 {{
                font-size: 14pt;
                color: #800000;
                padding-bottom: 5px;
            }}
            h3 {{
                font-size: 12pt;
                font-style: italic;
            }}
            p {{
                margin-bottom: 12px;
                text-align: justify;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    '''
    
    print(f"Generating PDF: {output_filename}...")
    
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html_content, dest=result_file)
        
    if pisa_status.err:
        print("An error occurred while generating the PDF.")
    else:
        print(f"PDF generated successfully! Saved as '{output_filename}'.")

if __name__ == "__main__":
    print("=" * 60)
    print("MSc ACADEMIC EXAMINATION ASSISTANT")
    print("=" * 60)
    
    # 1. Take user input for the prompt
    user_prompt = input("\nEnter your exam question: ").strip()
    
    if not user_prompt:
        print("Error: Question cannot be empty. Exiting script.")
        exit(1)
        
    # 2. Take user input for the filename
    user_filename = input("Enter a name to save the PDF (without the .pdf extension): ").strip()
    
    if not user_filename:
        user_filename = "Academic_Evaluation"
        print("No filename provided. Using default name.")
        
    final_filename = f"{user_filename}.pdf"
    
    # 3. Handle the "Answers" directory creation
    target_folder = "Answers"
    os.makedirs(target_folder, exist_ok=True)
    
    # Create the full path by joining the folder name and file name
    final_output_path = os.path.join(target_folder, final_filename)
    
    # 4. Call Groq API
    response = ask_groq_academic(user_prompt)
    
    if response:
        print("Response received from Groq. Formatting and saving to PDF...")
        
        # Prepare content for PDF with dynamic title and updated keyword
        full_markdown = f"<h1>{user_filename}</h1>\n<p><strong>Question:</strong> <em>{user_prompt}</em></p>\n<hr>\n\n" + response
        
        # Generate the PDF file at the specific folder path!
        save_markdown_to_pdf(full_markdown, final_output_path)