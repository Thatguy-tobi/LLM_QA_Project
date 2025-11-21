import streamlit as st
import re
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="NLP Q&A System", page_icon="🤖")

# --- PREPROCESSING FUNCTION ---
def preprocess_text(text):
    """Applies lowercasing, punctuation removal, and tokenization."""
    text_lower = text.lower()
    text_clean = re.sub(r'[^\w\s]', '', text_lower)
    tokens = text_clean.split()
    return text_clean, tokens

# --- SIDEBAR FOR CONFIG ---
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# --- MAIN UI ---
st.title("🤖 NLP Q&A System")
st.markdown("Ask a question, view the preprocessing, and get an answer from the LLM.")

# User Input
user_question = st.text_area("Enter your question here:", height=100)

if st.button("Get Answer"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar.")
    elif not user_question:
        st.warning("Please enter a question.")
    else:
        try:
            # 1. Configure API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # 2. Preprocess
            cleaned_text, tokens = preprocess_text(user_question)

            # 3. Display Preprocessing Results (Requirement)
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.info("🔤 Processed Text (Cleaned)")
                st.write(cleaned_text)
            with col2:
                st.info("🧩 Tokens")
                st.write(tokens)

            # 4. Get Response
            with st.spinner("Consulting the LLM..."):
                response = model.generate_content(cleaned_text)
                answer = response.text

            # 5. Display Answer
            st.divider()
            st.success("💡 LLM Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"An error occurred: {e}")