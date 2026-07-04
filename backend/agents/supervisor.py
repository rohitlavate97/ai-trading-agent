import operator
from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.config import settings
from agents.tools import get_stock_price, get_portfolio_tools

# State definition
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# Schema for supervisor routing
class Route(BaseModel):
    next: Literal["MarketAgent", "PortfolioAgent", "FINISH"]

def get_supervisor_app(db: AsyncSession, user_id: str):
    """Build and compile the multi-agent supervisor graph."""
    
    # Check API Key
    if not settings.OPENAI_API_KEY:
        # Mock simple graph if no API key
        async def mock_agent(state: AgentState):
            return {"messages": [AIMessage(content="[MOCK] Supervisor routing disabled. OPENAI_API_KEY missing.")], "next": "FINISH"}
        
        workflow = StateGraph(AgentState)
        workflow.add_node("Supervisor", mock_agent)
        workflow.add_edge(START, "Supervisor")
        workflow.add_edge("Supervisor", END)
        return workflow.compile()
        
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.OPENAI_API_KEY)
    
    # 1. Create Sub-Agents
    market_agent = create_react_agent(
        llm, 
        tools=[get_stock_price],
        state_modifier="You are a Market Agent. You provide stock prices and market data. Answer concisely."
    )
    
    portfolio_tools = get_portfolio_tools(db, user_id)
    portfolio_agent = create_react_agent(
        llm, 
        tools=portfolio_tools,
        state_modifier="You are a Portfolio Agent. You manage the user's portfolio and orders. Answer concisely."
    )
    
    # Node wrappers for sub-agents to adapt state
    async def market_node(state: AgentState):
        result = await market_agent.ainvoke({"messages": state["messages"]})
        # Wrap response so supervisor knows who spoke
        msg = AIMessage(content=result["messages"][-1].content, name="MarketAgent")
        return {"messages": [msg]}
        
    async def portfolio_node(state: AgentState):
        result = await portfolio_agent.ainvoke({"messages": state["messages"]})
        msg = AIMessage(content=result["messages"][-1].content, name="PortfolioAgent")
        return {"messages": [msg]}
        
    # 2. Create Supervisor
    system_prompt = (
        "You are a supervisor managing a conversation between the following workers: {members}. "
        "Given the following user request, respond with the worker to act next. "
        "Each worker will perform a task and respond with their results and status. "
        "When finished responding to the user's request, output 'FINISH'."
    )
    options = ["MarketAgent", "PortfolioAgent", "FINISH"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}",
        ),
    ]).partial(options=str(options), members="MarketAgent, PortfolioAgent")
    
    supervisor_chain = prompt | llm.with_structured_output(Route)
    
    async def supervisor_node(state: AgentState):
        decision = await supervisor_chain.ainvoke({"messages": state["messages"]})
        return {"next": decision.next}
        
    # 3. Build Graph
    workflow = StateGraph(AgentState)
    
    workflow.add_node("MarketAgent", market_node)
    workflow.add_node("PortfolioAgent", portfolio_node)
    workflow.add_node("Supervisor", supervisor_node)
    
    # Edges
    workflow.add_edge("MarketAgent", "Supervisor")
    workflow.add_edge("PortfolioAgent", "Supervisor")
    
    workflow.add_conditional_edges(
        "Supervisor",
        lambda x: x["next"],
        {
            "MarketAgent": "MarketAgent",
            "PortfolioAgent": "PortfolioAgent",
            "FINISH": END
        }
    )
    
    workflow.add_edge(START, "Supervisor")
    
    return workflow.compile()

import json

async def stream_chat_with_supervisor(db: AsyncSession, user_id: str, message: str):
    """Generator to stream events from the supervisor agent"""
    app = get_supervisor_app(db, user_id)
    inputs = {"messages": [HumanMessage(content=message)]}
    
    if not settings.OPENAI_API_KEY:
        yield json.dumps({"type": "message", "content": "[MOCK] Supervisor routing disabled. OPENAI_API_KEY missing."})
        yield json.dumps({"type": "message_end"})
        return
        
    async for event in app.astream_events(inputs, version="v1"):
        kind = event["event"]
        
        # Stream LLM tokens
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield json.dumps({"type": "token", "content": content})
                
        # Stream Tool starts
        elif kind == "on_tool_start":
            yield json.dumps({
                "type": "tool_start", 
                "name": event["name"], 
                "input": event["data"].get("input")
            })
            
        # Stream Tool ends
        elif kind == "on_tool_end":
            yield json.dumps({
                "type": "tool_end", 
                "name": event["name"], 
                "result": str(event["data"].get("output"))
            })
            
    yield json.dumps({"type": "message_end"})
