import os
import re
import google.generativeai as genai

# --- CONFIGURATION ---
# In a real app, use environment variables. For this assignment, 
# we will ask the user for the key or hardcode it for testing.
api_key = input("Enter your Google Gemini API Key: ").strip()
genai.configure(api_key=api_key)

# Select the model
model = genai.GenerativeModel('gemini-1.5-flash')

def preprocess_input(text):
    """
    Performs: Lowercasing, Punctuation Removal, and Tokenization.
    Returns a tuple: (cleaned_string, list_of_tokens)
    """
    # 1. Lowercasing
    text = text.lower()
    
    # 2. Punctuation Removal (keeping only words and spaces)
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Tokenization (splitting by whitespace)
    tokens = text.split()
    
    return text, tokens

def main():
    print("\n--- NLP Q&A System (CLI) ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_question = input("You: ")
        
        if user_question.lower() == 'exit':
            print("Goodbye!")
            break

        # Preprocessing steps
        cleaned_text, tokens = preprocess_input(user_question)
        
        print(f"\n[Debug] Processed tokens: {tokens}")
        print("Thinking...")

        try:
            # Send to LLM API
            # We send the original question for better context, 
            # but the assignment asks to process it. 
            # Let's send the cleaned text to adhere to requirements.
            response = model.generate_content(cleaned_text)
            
            print(f"LLM: {response.text}\n")
            print("-" * 30)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()