from utils.task import (
    create_task_in_db,
    get_all_tasks,
    get_tasks_by_user,
    update_task_in_db,
    delete_task_in_db,
)
from fastapi import APIRouter, HTTPException, status
from schemas.schemas import TaskCreate, TaskResponse, TaskUpdate
from DB.database import db_dependency

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate, db: db_dependency):
    task = await create_task_in_db(db, task_create)

    return {"message": "Task created successfully", "task": task}


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(db: db_dependency):
    """
    Получение списка всех задач.
    """
    tasks = await get_all_tasks(db)
    return tasks


@router.get("/tasks/{user_id}", response_model=list[TaskResponse])
async def get_tasks_for_user(user_id: int, db: db_dependency):
    """
    Получение задач конкретного пользователя.
    """
    tasks = await get_tasks_by_user(db, user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found for this user")
    return tasks


@router.put("/tasks/{task_id}", response_model=TaskUpdate)
async def update_task(task_id: int, task_update: TaskUpdate, db: db_dependency):
    """
    Эндпоинт для обновления данных задачи.
    """
    updated_task = await update_task_in_db(db, task_id, task_update)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: db_dependency):
    """
    Эндпоинт для удаления задачи.
    """
    success = await delete_task_in_db(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
