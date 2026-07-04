from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from models.order import OrderType, OrderSide, OrderStatus

class OrderBase(BaseModel):
    symbol: str
    order_type: OrderType
    side: OrderSide
    quantity: Decimal
    price: Optional[Decimal] = None

class OrderCreate(OrderBase):
    pass

class OrderInDBBase(OrderBase):
    id: str
    portfolio_id: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Order(OrderInDBBase):
    pass
