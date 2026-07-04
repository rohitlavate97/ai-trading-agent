from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.user import User
from api.deps import get_current_active_user
from agents.base import chat_with_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Pass message to the LangGraph agent
    # Currently stateless, in the future we'll pass thread_id for conversation history
    response_text = await chat_with_agent(db, current_user.id, request.message)
    return ChatResponse(response=response_text)
