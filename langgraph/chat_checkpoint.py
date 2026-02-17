from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    resonspe = llm.invoke(state.get("messages"))
    return {"messages": [resonspe]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot) # "chatbot" is the node name we have given

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
    


DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)
    config = {
        "configurable": {
            "thread_id": "yash" #user_id -> This tracks the conversation history(messages and state) for a user
        }
    }

    for chunk in graph_with_checkpointer.stream(
        State({"messages": ["What am i learning?"]}),
        config=config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()