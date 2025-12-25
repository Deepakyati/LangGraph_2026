from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import OllamaLLM


#1-define state
class State(Dict):
    messages: List[Dict[str,str]]


#2-Initialize stategraph
graph_builder = StateGraph(State)


#3-initialize the LLM
llm = OllamaLLM(model="llama3.1")

#4-define chatbot function
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    state["messages"].append({"role":"assistant",
                              "content": response})
    
    return {"messages":state["messages"]}


#5-add nodes and edges
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


#6-compile the graph
graph = graph_builder.compile()

#7-Stream updates
def stream_graph_updates(user_input: str):
    #initialize the state with the user's input
    state = {"messages":[{"role":"user", "content":"user_input"}]}
    for event in graph.stream(state):
        for value in event.values():
            #print the assistant response
            print("Assistant:", value["messages"[-1]["content"]])
