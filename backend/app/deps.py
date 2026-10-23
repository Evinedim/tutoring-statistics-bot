from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.models import Tutor


async def get_telegram_id(telegram_id: int = Header(...), ) -> int:
    return telegram_id

async def get_current_tutor(
    telegram_id: int = Depends(get_telegram_id), 
    session: AsyncSession = Depends(get_session)
) -> Tutor:
    db_scalars = await session.scalars(
        select(Tutor).where(Tutor.telegram_id == telegram_id, Tutor.is_active == True)
    )
    db_tutor = db_scalars.first()
    if db_tutor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tutor not found or inactive"
            )
    return db_tutor