from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Date, Numeric, ForeignKey

from backend.app.database import Base


class Tutor(Base):
    __tablename__ = "tutors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    discipline: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="tutor")
    tutors_students: Mapped[list["TutorStudent"]] = relationship("TutorStudent", back_populates="tutor")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="student")
    tutors_students: Mapped[list["TutorStudent"]] = relationship("TutorStudent", back_populates="student")


class TutorStudent(Base):
    __tablename__ = "tutors_students"

    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)

    tutor: Mapped["Tutor"] = relationship("Tutor", back_populates="tutors_students")
    student: Mapped["Student"] = relationship("Student", back_populates="tutors_students")


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    lesson_date: Mapped[date] = mapped_column(Date, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    lessons_done: Mapped[int] = mapped_column(Integer, nullable=False)
    lessons_total: Mapped[int] = mapped_column(Integer, nullable=False)

    tutor: Mapped["Tutor"] = relationship("Tutor", back_populates="lessons")
    student: Mapped["Student"] = relationship("Student", back_populates="lessons")