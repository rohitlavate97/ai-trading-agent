from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import get_db
from models.user import User
from schemas.user import User as UserSchema
from api.deps import get_current_active_user, require_role
from models.user import RoleEnum

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.get("", response_model=List[UserSchema], dependencies=[Depends(require_role(RoleEnum.ADMIN))])
async def read_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
