import streamlit as st
import os
from dotenv import load_dotenv
from utils.code_splitter import SQLCodeSplitter
from utils.llm_handler import LLMHandler
import asyncio

# Load environment variables
load_dotenv()

# Initialize components
code_splitter = SQLCodeSplitter(
    chunk_size=int(os.getenv("CHUNK_SIZE")),
    chunk_overlap=int(os.getenv("CHUNK_OVERLAP"))
)
llm_handler = LLMHandler()

st.title("SQL Code Explainer")

# Add a file uploader or text area for SQL input
input_method = st.radio(
    "Choose input method:",
    ("Text Input", "File Upload")
)

sql_code = ""

if input_method == "Text Input":
    sql_code = st.text_area("Enter your SQL code:", height=300)
else:
    uploaded_file = st.file_uploader("Upload SQL file", type=['sql'])
    if uploaded_file:
        sql_code = uploaded_file.getvalue().decode()

if st.button("Explain Code") and sql_code:
    with st.spinner("Analyzing SQL code..."):
        # Split code into chunks
        chunks = code_splitter.split_sql_code(sql_code)
        
        # Create progress bar
        progress_bar = st.progress(0)
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            st.subheader(f"Section {i+1}")
            st.code(chunk, language="sql")
            
            # Get explanation
            explanation = asyncio.run(llm_handler.explain_code_chunk(chunk))
            st.write(explanation)
            
            # Update progress
            progress_bar.progress((i + 1) / len(chunks))
            
        st.success("Analysis complete!")