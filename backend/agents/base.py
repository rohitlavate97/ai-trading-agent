from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from agents.tools import get_stock_price, get_portfolio_tools

# Define the state for the agent
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]

def get_agent_app(db: AsyncSession, user_id: str):
    """Build and compile the LangGraph app with bound tools."""
    portfolio_tools = get_portfolio_tools(db, user_id)
    all_tools = [get_stock_price] + portfolio_tools
    
    # Node: Call the LLM
    async def call_model(state: AgentState):
        messages = state["messages"]
        
        # Simple mock if no API key is provided during dev
        if not settings.OPENAI_API_KEY:
            response = AIMessage(content="[MOCK] This is a mocked LLM response since OPENAI_API_KEY is not set.")
            return {"messages": [response]}
            
        model = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.OPENAI_API_KEY)
        model_with_tools = model.bind_tools(all_tools)
        response = await model_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Build the graph
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(all_tools))
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

async def chat_with_agent(db: AsyncSession, user_id: str, message: str) -> str:
    """Convenience function to interact with the basic agent"""
    app = get_agent_app(db, user_id)
    inputs = {"messages": [HumanMessage(content=message)]}
    
    # Process the stream
    async for output in app.astream(inputs):
        for key, value in output.items():
            pass # Consume stream to get final result
            
    # Return the last message content
    return value["messages"][-1].content
