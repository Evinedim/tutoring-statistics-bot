from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class TutorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя репетитора (2-50 символов)")
    discipline: str = Field(..., min_length=2, max_length=50, description="Название преподаваемой дисциплины")

class TutorRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор репетитора")
    telegram_id: int = Field(..., description="Уникальный идентификатор репетитора в Telegram")
    name: str = Field(..., description="Имя репетитора (2-50 символов)")
    discipline: str = Field(..., description="Название преподаваемой дисциплины")
    is_active: bool = Field(..., description="Активен ли репетитор")

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя ученика (2-50 символов)")
    grade: int = Field(..., ge=1, le=11, description="Класс ученика (от 1 до 11)")

class StudentRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор ученика")
    name: str = Field(..., description="Имя ученика (2-50 символов)")
    grade: int = Field(..., description="Класс ученика (от 1 до 11)")
    is_active: bool = Field(..., description="Активен ли ученик")

    model_config = ConfigDict(from_attributes=True)


class LessonCreate(BaseModel):
    tutor_id: int = Field(..., description="Уникальный идентификатор репетитора")
    student_id: int = Field(..., description="Уникальный идентификатор ученика")
    lesson_date: date = Field(..., description="Дата занятия")
    duration: int = Field(..., description="Длительность занятия в минутах")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Цена занятия")
    lessons_done: int = Field(..., description="Количество занятий, проведённых по абонементу")
    lessons_total: int = Field(..., description="Количество занятий в абонементе")

class LessonRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор занятия")
    tutor_id: int = Field(..., description="Уникальный идентификатор репетитора")
    student_id: int = Field(..., description="Уникальный идентификатор ученика")
    lesson_date: date = Field(..., description="Дата занятия")
    duration: int = Field(..., description="Длительность занятия в минутах")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Цена занятия")
    lessons_done: int = Field(..., description="Количество занятий, проведённых по абонементу")
    lessons_total: int = Field(..., description="Количество занятий в абонементе")

    model_config = ConfigDict(from_attributes=True)