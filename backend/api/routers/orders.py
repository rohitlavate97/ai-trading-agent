from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.user import User
from api.deps import get_current_active_user
from schemas.order import Order, OrderCreate
from services import portfolio_service

router = APIRouter()

@router.get("", response_model=List[Order])
async def read_orders(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    portfolio = await portfolio_service.get_portfolio_by_user(db, user_id=current_user.id)
    return await portfolio_service.get_orders_by_portfolio(db, portfolio_id=portfolio.id)

@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
async def submit_order(
    order_in: OrderCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    portfolio = await portfolio_service.get_portfolio_by_user(db, user_id=current_user.id)
    try:
        order = await portfolio_service.submit_order(db, portfolio_id=portfolio.id, order_in=order_in)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
