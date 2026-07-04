from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.watchlist import Watchlist, WatchlistItem
from schemas.watchlist import WatchlistCreate, WatchlistUpdate, WatchlistItemCreate

async def create_watchlist(db: AsyncSession, user_id: str, obj_in: WatchlistCreate) -> Watchlist:
    db_obj = Watchlist(user_id=user_id, name=obj_in.name, description=obj_in.description)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_watchlists_by_user(db: AsyncSession, user_id: str) -> List[Watchlist]:
    result = await db.execute(
        select(Watchlist).options(selectinload(Watchlist.items)).where(Watchlist.user_id == user_id)
    )
    return list(result.scalars().all())

async def get_watchlist(db: AsyncSession, watchlist_id: str) -> Optional[Watchlist]:
    result = await db.execute(
        select(Watchlist).options(selectinload(Watchlist.items)).where(Watchlist.id == watchlist_id)
    )
    return result.scalars().first()

async def add_item_to_watchlist(db: AsyncSession, watchlist_id: str, item_in: WatchlistItemCreate) -> WatchlistItem:
    # Ensure no duplicates in the same watchlist
    result = await db.execute(
        select(WatchlistItem).where(WatchlistItem.watchlist_id == watchlist_id, WatchlistItem.symbol == item_in.symbol)
    )
    existing = result.scalars().first()
    if existing:
        return existing

    db_obj = WatchlistItem(watchlist_id=watchlist_id, symbol=item_in.symbol)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove_item_from_watchlist(db: AsyncSession, watchlist_id: str, symbol: str) -> bool:
    result = await db.execute(
        select(WatchlistItem).where(WatchlistItem.watchlist_id == watchlist_id, WatchlistItem.symbol == symbol)
    )
    obj = result.scalars().first()
    if obj:
        await db.delete(obj)
        await db.commit()
        return True
    return False
