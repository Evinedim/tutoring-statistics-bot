from datetime import date

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from backend.app.database import get_session
from backend.app.schemas import LessonCreate, LessonRead
from backend.app.models import Tutor, Student, Lesson
from backend.app.deps import get_current_tutor, get_student


router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

@router.post("/students/{student_id}", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson: LessonCreate,
    student: Student = Depends(get_student),
    tutor: Tutor = Depends(get_current_tutor),
    session: AsyncSession = Depends(get_session)
):
    db_lesson = Lesson(tutor_id=tutor.id, student_id=student.id, **lesson.model_dump())
    session.add(db_lesson)
    await session.commit()
    await session.refresh(db_lesson)
    return db_lesson

@router.get("/", response_model=list[LessonRead])
async def get_lessons(
    start_date: date, 
    end_date: date,
    tutor: Tutor = Depends(get_current_tutor),
    session: AsyncSession = Depends(get_session)
):
    db_scalars = await session.scalars(
        select(Lesson).where(
            Lesson.tutor_id == tutor.id, 
            Lesson.lesson_date.between(start_date, end_date)
        )
    )
    return db_scalars.all()

@router.put("/{lesson_id}", response_model=LessonRead)
async def update_lesson(
    lesson_id: int,
    lesson: LessonCreate,
    tutor: Tutor = Depends(get_current_tutor),
    session: AsyncSession = Depends(get_session)
):
    db_scalars = await session.scalars(
        select(Lesson).where(Lesson.id == lesson_id, Lesson.tutor_id == tutor.id)
    )
    db_lesson = db_scalars.first()
    if db_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    for field, value in lesson.model_dump().items():
        setattr(db_lesson, field, value)

    await session.commit()
    await session.refresh(db_lesson)
    return db_lesson

@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
    lesson_id: int, 
    tutor: Tutor = Depends(get_current_tutor), 
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        delete(Lesson).where(Lesson.id == lesson_id, Lesson.tutor_id == tutor.id)
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    await session.commit()