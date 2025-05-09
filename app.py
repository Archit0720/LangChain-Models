from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama 

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # typo was here
#prompting

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a chatbot and your theme is anime related , you will answer all queries in anime style "),
    ("user", "question:{question}")
])


st.title("Tutorial-1 Langchain")
input_text=st.text_input("enter the question")

llm=Ollama(model="llama2")
Output_Parser=StrOutputParser()
chain=prompt|llm|Output_Parser

if input_text:
    st.write(chain.invoke({"question":input_text}))
