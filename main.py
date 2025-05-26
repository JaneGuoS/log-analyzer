import streamlit as st
import os
import torch

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 

# or simply:
torch.classes.__path__ = []
from analyzer import log_analyzer



# Streamlit app
def main():

    st.title("RAG Based Log Analyzer 📊")
    st.write("Welcome to the Log Analyzer! You can use this app analyze the log.")


    try:
        # Get the prompt
        userPrompt = st.text_area("Enter your question for the log:")

        #Get the codes queried by the prompt
        if st.button("Analyze"):
            result_placeholder = st.empty()
            result_placeholder.write("🧑‍💻 Analyzing...")

            result = log_analyzer.chat_with_llm(userPrompt, [], 'llama2')
            result_placeholder.write(result)

    except Exception as e:
        st.error(f"An error occurred: {e}")
if __name__ == "__main__":
    main()
