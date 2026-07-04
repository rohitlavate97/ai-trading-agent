from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PositionBase(BaseModel):
    symbol: str
    quantity: Decimal
    average_price: Decimal

class PositionInDBBase(PositionBase):
    id: str
    portfolio_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Position(PositionInDBBase):
    pass

class PortfolioBase(BaseModel):
    cash_balance: Decimal

class PortfolioInDBBase(PortfolioBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Portfolio(PortfolioInDBBase):
    positions: List[Position] = []
