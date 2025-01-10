from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from DB.models import User
from fastapi import HTTPException
from schemas.schemas import UserCreate


async def create_user_in_db(db: AsyncSession, user_create: UserCreate):
    """
    Функция для создания пользователя в базе данных.
    """
    # Создаем объект пользователя
    user = User(
        username=user_create.username,
        email=user_create.email,
    )
    try:
        db.add(user)
        await db.commit()
        return user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

async def get_user_from_db(db: AsyncSession, user_id: int):
    """
    Функция ля полученияя пользователя
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    print(f"User found: {user}") 
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user