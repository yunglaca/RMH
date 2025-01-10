from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Базовый класс с общей конфигурацией
class BaseConfig(BaseModel):
    class Config:
        from_attributes = True

class UserCreate(BaseConfig):
    username: str
    email: EmailStr

class UserResponse(BaseConfig):
    id: int
    username: str
    email: EmailStr
    tasks: List["TaskResponse"] = []  # Включаем связанные задачи для отображения

class TaskCreate(BaseConfig):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    user_id: int  # ID пользователя, которому принадлежит задача

class TaskResponse(BaseConfig):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    user_id: int  # ID пользователя, которому принадлежит задача

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: date | None = None