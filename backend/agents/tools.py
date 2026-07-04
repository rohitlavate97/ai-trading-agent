import random
from langchain_core.tools import tool
from sqlalchemy.ext.asyncio import AsyncSession
from services.portfolio_service import get_portfolio_by_user

@tool
def get_stock_price(symbol: str) -> dict:
    """Get the current stock price for a given symbol."""
    # Mocking price for now. In a real app, integrate with Alpaca or Polygon.io
    base_price = sum(ord(c) for c in symbol) # Deterministic mock base
    random_variation = random.uniform(-0.05, 0.05)
    current_price = base_price * (1 + random_variation)
    
    return {
        "symbol": symbol.upper(),
        "price": round(current_price, 2),
        "currency": "USD"
    }

from db.vector import get_qdrant_client, COLLECTION_NAME, VECTOR_SIZE

@tool
def search_company_filings(query: str, symbol: str = None) -> str:
    """
    Search through SEC company filings (10-K, 10-Q) and earnings transcripts for insights.
    Useful for answering questions about a company's risks, supply chain, or strategy.
    """
    try:
        client = get_qdrant_client()
        # In a real RAG system, we would embed the `query` string using OpenAI embeddings:
        # embeddings = OpenAIEmbeddings()
        # vector = embeddings.embed_query(query)
        # For this milestone, we use a dummy vector to fetch the seeded data
        dummy_vector = [0.015] * VECTOR_SIZE
        
        search_filter = None
        if symbol:
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            search_filter = Filter(
                must=[FieldCondition(key="symbol", match=MatchValue(value=symbol.upper()))]
            )
            
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=dummy_vector,
            query_filter=search_filter,
            limit=3
        )
        
        if not results:
            return f"No filings found matching query for {symbol or 'any company'}."
            
        context = []
        for r in results:
            payload = r.payload or {}
            context.append(f"[{payload.get('symbol')} {payload.get('document_type')}]: {payload.get('content')}")
            
        return "\n\n".join(context)
    except Exception as e:
        return f"Failed to search filings: {str(e)}"

def get_portfolio_tools(db: AsyncSession, user_id: str):
    """Factory to inject db session and user_id into tools."""
    
    @tool
    async def get_portfolio_summary() -> dict:
        """Get the current user's portfolio cash balance and active positions."""
        portfolio = await get_portfolio_by_user(db, user_id)
        
        positions_list = []
        for pos in portfolio.positions:
            positions_list.append({
                "symbol": pos.symbol,
                "quantity": float(pos.quantity),
                "average_price": float(pos.average_price)
            })
            
        return {
            "cash_balance": float(portfolio.cash_balance),
            "positions": positions_list
        }
        
    return [get_portfolio_summary]

def get_market_tools():
    return [get_stock_price, search_company_filings]
