from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # 👈 Import Groq integration

load_dotenv()

# Load environment variables
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # typo was here

# FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# Initialize Groq model
groq_model = ChatGroq(
    model_name="mixtral-8x7b-32768",  # or "llama3-70b-8192", depending on what you want
    api_key=os.getenv("GROQ_API_KEY")
)

# Add route using Groq
add_routes(
    app,
    groq_model,
    path="/groq"
)

# Ollama model
llm = Ollama(model="llama2")

# Prompts
prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} for a 5 years child with 100 words")

# Route for essay using Groq
add_routes(
    app,
    prompt1 | groq_model,
    path="/essay"
)

# Route for poem using Ollama
add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
