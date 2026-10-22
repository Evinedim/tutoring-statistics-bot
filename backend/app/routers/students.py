from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.models import Student, Tutor
from backend.app.schemas import StudentCreate, StudentRead


router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.post("/tutors/{telegram_id}", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(telegram_id: int, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    db_scalars = await session.scalars(
        select(Tutor).where(Tutor.telegram_id == telegram_id, Tutor.is_active == True)
    )
    db_teacher = db_scalars.first()
    if db_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tutor with such telegram id has not found"
            )

    db_student = Student(**student.model_dump())
    db_student.tutors.append(db_teacher)

    session.add(db_student)
    await session.commit()
    await session.refresh(db_student)

    return db_student

@router.get("/", response_model=list[StudentRead])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    db_scalars = await session.scalars(
        select(Student).where(Student.is_active == True)
    )
    db_students = db_scalars.all()
    return db_students