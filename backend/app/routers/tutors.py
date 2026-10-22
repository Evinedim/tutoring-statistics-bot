from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.schemas import TutorCreate, TutorRead
from backend.app.models import Tutor


router = APIRouter(
    prefix="/tutors",
    tags=["tutors"]
)

@router.post("/{telegram_id}", response_model=TutorRead, status_code=status.HTTP_201_CREATED)
async def create_tutor(telegram_id: int, tutor: TutorCreate, session: AsyncSession = Depends(get_session)):
    db_scalars = await session.scalars(
        select(Tutor).where(Tutor.telegram_id == telegram_id)
    )
    if db_scalars.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tutor with such telegram id has already existed"
            )

    db_tutor = Tutor(telegram_id=telegram_id, name=tutor.name, discipline=tutor.discipline)

    session.add(db_tutor)
    await session.commit()
    await session.refresh(db_tutor)

    return db_tutor

@router.get("/", response_model=list[TutorRead])
async def get_all_tutors(session: AsyncSession = Depends(get_session)):
    db_scalars = await session.scalars(
        select(Tutor).where(Tutor.is_active == True)
    )
    db_tutors = db_scalars.all()
    return db_tutors