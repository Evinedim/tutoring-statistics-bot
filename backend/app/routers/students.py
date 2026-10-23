from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.app.database import get_session
from backend.app.models import Student, Tutor
from backend.app.schemas import StudentCreate, StudentRead
from backend.app.deps import get_current_tutor, get_student


router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreate, 
    db_tutor: Tutor = Depends(get_current_tutor), 
    session: AsyncSession = Depends(get_session)
):
    db_student = Student(**student.model_dump())
    db_student.tutors.append(db_tutor)

    session.add(db_student)
    await session.commit()
    await session.refresh(db_student)

    return db_student

@router.get("/", response_model=list[StudentRead])
async def get_all_students(
    db_tutor: Tutor = Depends(get_current_tutor), 
    session: AsyncSession = Depends(get_session)
):
    db_scalars = await session.scalars(
        select(Student).where(Student.tutors.any(Tutor.id == db_tutor.id), Student.is_active == True)
    )
    db_students = db_scalars.all()
    return db_students

@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student: StudentCreate,
    db_student: Student = Depends(get_student),
    session: AsyncSession = Depends(get_session)
):
    db_student.name, db_student.grade = student.name, student.grade
    await session.commit()
    await session.refresh(db_student)
    return db_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    db_student: Student = Depends(get_student),
    session: AsyncSession = Depends(get_session)
):
    db_student.is_active = False
    await session.commit()