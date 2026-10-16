from pydantic import BaseModel, Field, ConfigDict


class TutorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя репетитора (2-50 символов)")
    discipline: str = Field(..., min_length=2, max_length=50, description="Название преподаваемой дисциплины")

class TutorRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор репетитора")
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