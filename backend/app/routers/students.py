from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.models import Student
from backend.app.schemas import StudentCreate, StudentRead


router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    db_student = Student(**student.model_dump())

    session.add(db_student)
    await session.commit()
    session.refresh(db_student)

    return db_student

@router.get("/", response_model=list[StudentRead])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    db_students = await session.scalars(
        select(Student).where(Student.is_active == True)
    )
    return db_students