from typing import Annotated
from fastapi import APIRouter, Depends
from models.user import User
from schemas.user import User as UserSchema
from api.deps import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
