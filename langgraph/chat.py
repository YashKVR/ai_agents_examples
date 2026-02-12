from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    resonspe = llm.invoke(state.get("messages"))
    return {"messages": [resonspe]}

def samplenode(state: State):
    print("\n\nSample node called with state:", state)
    return {"messages": ["Hi, This is a message from the sample node"]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot) # "chatbot" is the node name we have given
graph_builder.add_node("samplenode", samplenode) # "samplenode" is the node name we have given

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke({"messages": ["Hi, This is a message from the user"]})
print("\n\nUpdated state:", updated_state)