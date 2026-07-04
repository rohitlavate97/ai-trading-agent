from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.user import User
from api.deps import get_current_active_user
from schemas.portfolio import Portfolio
from services import portfolio_service

router = APIRouter()

@router.get("", response_model=Portfolio)
async def read_portfolio(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await portfolio_service.get_portfolio_by_user(db, user_id=current_user.id)
