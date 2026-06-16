from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

print("API Key Loaded:", os.getenv("OPENROUTER_API_KEY") is not None)

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = llm.invoke("What is LangGraph?")

print(response.content)