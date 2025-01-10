from DB.config import settings
from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from typing import Annotated
from fastapi import Depends

DATABASE_URL = settings.database_url

engine = create_async_engine(url=DATABASE_URL,echo=False)

async_session_maker = async_sessionmaker(engine,expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session

db_dependency = Annotated[AsyncSession, Depends(get_db)]

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"