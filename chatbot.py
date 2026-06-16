from typing import TypedDict, Annotated

from dotenv import load_dotenv
import os

from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages


load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = [
        SystemMessage(
            content="""
            You are a helpful AI assistant.
            Always respond in English.
            Never respond in Chinese or any other language unless explicitly requested.
            """
        )
    ] + state["messages"]
    response = llm.invoke(messages)
    return {"messages" : [response]}

#Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)