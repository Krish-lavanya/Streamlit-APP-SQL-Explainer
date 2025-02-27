from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List
import os

class LLMHandler:
    def __init__(self):
        self.llm = Ollama(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            model=os.getenv("MODEL_NAME"),
            temperature=0.1
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["sql_code"],
            template="""
            You are an expert SQL developer. Please explain the following SQL code in detail:
            What it does, its purpose, and break down the important components.
            
            SQL CODE:
            {sql_code}
            
            Provide a detailed explanation including:
            1. Overall purpose
            2. Main components and their functions
            4. Any potential performance considerations
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    async def explain_code_chunk(self, chunk: str) -> str:
        try:
            explanation = await self.chain.arun(sql_code=chunk)
            return explanation
        except Exception as e:
            return f"Error processing chunk: {str(e)}"