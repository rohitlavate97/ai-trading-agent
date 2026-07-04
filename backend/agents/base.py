from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from core.config import settings

# Define the state for the agent
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]

# Node: Call the LLM
async def call_model(state: AgentState):
    messages = state["messages"]
    
    # Simple mock if no API key is provided during dev
    if not settings.OPENAI_API_KEY:
        response = AIMessage(content="[MOCK] This is a mocked LLM response since OPENAI_API_KEY is not set.")
        return {"messages": [response]}
        
    # Real LLM call
    model = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.OPENAI_API_KEY)
    response = await model.ainvoke(messages)
    return {"messages": [response]}

# Build the graph
workflow = StateGraph(AgentState)

# Add the single node
workflow.add_node("agent", call_model)

# Set entry point
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Compile
app = workflow.compile()

async def chat_with_agent(message: str) -> str:
    """Convenience function to interact with the basic agent"""
    inputs = {"messages": [HumanMessage(content=message)]}
    async for output in app.astream(inputs):
        for key, value in output.items():
            pass # Just consume the stream
    
    # Return the last message content
    return value["messages"][-1].content
