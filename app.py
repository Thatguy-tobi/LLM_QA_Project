from flask import Flask, render_template, request
import google.generativeai as genai
import re
import os

app = Flask(__name__)

def preprocess_text(text):
    """Applies lowercasing, punctuation removal, and tokenization."""
    text_lower = text.lower()
    text_clean = re.sub(r'[^\w\s]', '', text_lower)
    tokens = text_clean.split()
    return text_clean, tokens

@app.route('/', methods=['GET', 'POST'])
def index():
    context = {}
    
    if request.method == 'POST':
        # Get data from the HTML form
        api_key = request.form.get('api_key')
        user_question = request.form.get('question')

        if not api_key or not user_question:
            context['error'] = "Please provide both an API Key and a Question."
        else:
            try:
                # 1. Configure API
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                # 2. Preprocess
                cleaned_text, tokens = preprocess_text(user_question)

                # 3. Get Response from LLM
                response = model.generate_content(cleaned_text)
                answer = response.text

                # 4. Save results to context to display in HTML
                context['original_question'] = user_question
                context['cleaned_text'] = cleaned_text
                context['tokens'] = tokens
                context['answer'] = answer

            except Exception as e:
                context['error'] = f"An error occurred: {e}"

    return render_template('index.html', **context)

if __name__ == '__main__':
    # Run locally
    app.run(debug=True)