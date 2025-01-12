from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from DB.models import Task
from schemas.schemas import TaskCreate, TaskUpdate


async def create_task_in_db(db: AsyncSession, task_create: TaskCreate):
    """
    Функция для создания задачи в базе данных.
    """
    task = Task(
        title=task_create.title,
        description=task_create.description,
        due_date=task_create.due_date,
        user_id=task_create.user_id,
    )

    db.add(task)
    await db.commit()
    return task


async def get_all_tasks(db: AsyncSession):
    """
    Функция для получения всех задач из базы данных.
    """
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks


async def get_tasks_by_user(db: AsyncSession, user_id: int):
    """
    Функция для получения задач конкретного пользователя по user_id.
    """
    result = await db.execute(select(Task).filter(Task.user_id == user_id))
    tasks = result.scalars().all()
    return tasks


async def update_task_in_db(db: AsyncSession, task_id: int, task_update: TaskUpdate):
    """
    Функция для обновления данных задачи в базе данных.
    """
    # Получаем задачу по ID
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        return None  

    # Обновляем только те поля, которые были переданы
    if task_update.title:
        task.title = task_update.title
    if task_update.description:
        task.description = task_update.description
    if task_update.due_date:
        task.due_date = task_update.due_date # type: ignore


    db.add(task)
    await db.commit()
    return task


async def delete_task_in_db(db: AsyncSession, task_id: int) -> bool:
    """
    Функция для удаления задачи из базы данных.
    """
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        return False

    await db.delete(task)
    await db.commit()
    return True
