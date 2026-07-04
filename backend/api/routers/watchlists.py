from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.user import User
from api.deps import get_current_active_user
from schemas.watchlist import Watchlist, WatchlistCreate, WatchlistItemCreate, WatchlistItem
from services import watchlist_service

router = APIRouter()

@router.post("", response_model=Watchlist, status_code=status.HTTP_201_CREATED)
async def create_watchlist(
    watchlist_in: WatchlistCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await watchlist_service.create_watchlist(db, user_id=current_user.id, obj_in=watchlist_in)

@router.get("", response_model=List[Watchlist])
async def read_watchlists(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await watchlist_service.get_watchlists_by_user(db, user_id=current_user.id)

@router.post("/{watchlist_id}/items", response_model=WatchlistItem, status_code=status.HTTP_201_CREATED)
async def add_item(
    watchlist_id: str,
    item_in: WatchlistItemCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    watchlist = await watchlist_service.get_watchlist(db, watchlist_id=watchlist_id)
    if not watchlist or watchlist.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    return await watchlist_service.add_item_to_watchlist(db, watchlist_id=watchlist_id, item_in=item_in)

@router.delete("/{watchlist_id}/items/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(
    watchlist_id: str,
    symbol: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    watchlist = await watchlist_service.get_watchlist(db, watchlist_id=watchlist_id)
    if not watchlist or watchlist.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    success = await watchlist_service.remove_item_from_watchlist(db, watchlist_id=watchlist_id, symbol=symbol)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in watchlist")
