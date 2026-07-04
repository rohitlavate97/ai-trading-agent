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
