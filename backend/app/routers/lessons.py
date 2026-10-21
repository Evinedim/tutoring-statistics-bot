from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.schemas import LessonCreate, LessonRead
from backend.app.models import Tutor, Student, Lesson


router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

@router.post("/", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
async def create_lesson(lesson: LessonCreate, session: AsyncSession = Depends(get_session)):
    db_scalars = await session.scalars(
        select(Tutor).where(Tutor.id == lesson.tutor_id, Tutor.is_active == True)
    )
    if db_scalars.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tutor not found or inactive")

    db_scalars = await session.scalars(
        select(Student).where(Student.id == lesson.student_id, Student.is_active == True)
    )
    if db_scalars.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not found or inactive")

    db_lesson = Lesson(**lesson.model_dump())
    session.add(db_lesson)
    await session.commit()
    await session.refresh(db_lesson)

    return db_lesson

@router.get("/", response_model=list[LessonRead])
async def get_all_lessons(session: AsyncSession = Depends(get_session)):
    db_scalars = await session.scalars(select(Lesson))
    return db_scalars.all()