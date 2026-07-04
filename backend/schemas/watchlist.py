from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class WatchlistItemBase(BaseModel):
    symbol: str

class WatchlistItemCreate(WatchlistItemBase):
    pass

class WatchlistItemInDBBase(WatchlistItemBase):
    id: str
    watchlist_id: str
    added_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class WatchlistItem(WatchlistItemInDBBase):
    pass

class WatchlistBase(BaseModel):
    name: str
    description: Optional[str] = None

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class WatchlistInDBBase(WatchlistBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Watchlist(WatchlistInDBBase):
    items: List[WatchlistItem] = []
