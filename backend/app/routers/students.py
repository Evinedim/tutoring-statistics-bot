from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.database import get_session
from backend.app.models import Student, Tutor
from backend.app.schemas import StudentCreate, StudentRead
from backend.app.deps import get_current_tutor


router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreate, 
    tutor: Tutor = Depends(get_current_tutor), 
    session: AsyncSession = Depends(get_session)
):
    db_student = Student(**student.model_dump())
    db_student.tutors.append(tutor)

    session.add(db_student)
    await session.commit()
    await session.refresh(db_student)

    return db_student

@router.get("/", response_model=list[StudentRead])
async def get_all_students(
    tutor: Tutor = Depends(get_current_tutor), 
    session: AsyncSession = Depends(get_session)
):
    db_scalars = await session.scalars(
        select(Student).where(Student.tutors.any(Tutor.id == tutor.id), Student.is_active == True)
    )
    db_students = db_scalars.all()
    return db_students