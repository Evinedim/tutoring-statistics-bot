from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.models import Tutor, Student


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

async def get_student(
    student_id: int,
    tutor: Tutor = Depends(get_current_tutor),
    session: AsyncSession = Depends(get_session)
) -> Student:
    db_scalars = await session.scalars(
        select(Student).where(
            Student.id == student_id,
            Student.tutors.any(Tutor.id == tutor.id),
            Student.is_active == True
        )
    )
    db_student = db_scalars.first()
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student