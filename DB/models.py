from DB.database import Base
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    # Связь с задачами
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="all, delete-orphan"
    )


class Task(Base):
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    due_date: Mapped[Date] = mapped_column(Date, default=None)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Связь с пользователем
    user: Mapped["User"] = relationship("User", back_populates="tasks")
