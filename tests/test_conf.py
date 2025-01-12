import pytest
import pytest_asyncio
import asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import sessionmaker
from datetime import date

from main import app
from DB.config import settings
from DB.models import User, Task
from DB.database import Base


@pytest_asyncio.fixture
async def async_client():
    """Фикстура для асинхронного клиента FastAPI."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


# Фикстура для цикла событий, который будет использоваться для асинхронных тестов
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_session(event_loop):

    async_engine = create_async_engine(settings.test_database_url, echo=True)
    session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        yield session  

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


# Тест для создания пользователя
@pytest.mark.asyncio
async def test_create_user(async_client, async_session: AsyncSession):
    user_data = {"username": "newuser", "email": "newuser@example.com"}
    response = await async_client.post("/users/", json=user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["message"] == "User created successfully"
    assert response_data["user"]["username"] == user_data["username"]
    assert response_data["user"]["email"] == user_data["email"]


# Тест для получения пользователя
@pytest.mark.asyncio
async def test_get_user(async_client, async_session: AsyncSession):
    user = User(username="existinguser", email="existinguser@example.com")
    async_session.add(user)
    await async_session.commit()

    response = await async_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == user.username
    assert response_data["email"] == user.email

# Тест для создания таски
@pytest.mark.asyncio
async def test_create_task(async_client, async_session: AsyncSession):
    user = User(username="testuser", email="testuser@example.com")
    async_session.add(user)
    await async_session.commit()

    task_data = {
        "title": "Test Task",
        "description": "Test task description",
        "user_id": user.id,
        "due_date": str(date(2025, 12, 31)),  #рандом дата
    }

    response = await async_client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["message"] == "Task created successfully"
    assert response_data["task"]["title"] == task_data["title"]
    assert response_data["task"]["description"] == task_data["description"]
    assert response_data["task"]["user_id"] == task_data["user_id"]
    assert response_data["task"]["due_date"] == task_data["due_date"]

# Тест для получения таски
@pytest.mark.asyncio
async def test_get_tasks(async_client, async_session: AsyncSession):
    user = User(username="testuser", email="testuser@example.com")
    async_session.add(user)
    await async_session.commit()

    task1 = Task(
        title="Test Task 1",
        description="Description 1",
        user_id=user.id,
        due_date=date(2025, 12, 31),
    )
    task2 = Task(
        title="Test Task 2",
        description="Description 2",
        user_id=user.id,
        due_date=date(2025, 12, 31),
    )
    async_session.add_all([task1, task2])
    await async_session.commit()

    response = await async_client.get("/tasks/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == task1.title
    assert tasks[1]["title"] == task2.title
    assert tasks[0]["due_date"] == str(task1.due_date)  
    assert tasks[1]["due_date"] == str(task2.due_date)  #две проверки

# Тест для получение таски для юзера
@pytest.mark.asyncio
async def test_get_tasks_for_user(async_client, async_session: AsyncSession):
    user = User(username="testuser", email="testuser@example.com")
    async_session.add(user)
    await async_session.commit()

    task = Task(
        title="User Task",
        description="User task description",
        user_id=user.id,
        due_date=date(2025, 12, 31),
    )
    async_session.add(task)
    await async_session.commit()

    response = await async_client.get(f"/tasks/tasks/{user.id}")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == task.title
    assert tasks[0]["due_date"] == str(task.due_date)  # Проверяем due_date

#тест для обновления таски
@pytest.mark.asyncio
async def test_update_task(async_client, async_session: AsyncSession):
    # Создаем пользователя и задачу
    user = User(username="testuser", email="testuser@example.com")
    async_session.add(user)
    await async_session.commit()

    task = Task(
        title="Old Task",
        description="Old description",
        user_id=user.id,
        due_date=date(2025, 12, 31),
    )
    async_session.add(task)
    await async_session.commit()

    task_update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "due_date": str(date(2025, 12, 30)),  # Обновленная дата
    }

    response = await async_client.put(f"/tasks/tasks/{task.id}", json=task_update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == task_update_data["title"]
    assert updated_task["description"] == task_update_data["description"]
    assert (
        updated_task["due_date"] == task_update_data["due_date"]
    )  

#тест удаление таски
@pytest.mark.asyncio
async def test_delete_task(async_client, async_session: AsyncSession):
    # Создаем пользователя и задачу
    user = User(username="testuser", email="testuser@example.com")
    async_session.add(user)
    await async_session.commit()

    task = Task(
        title="Task to Delete",
        description="Description",
        user_id=user.id,
        due_date=date(2025, 12, 31),
    )
    async_session.add(task)
    await async_session.commit()

    response = await async_client.delete(f"/tasks/tasks/{task.id}")
    assert response.status_code == 204

    # Проверяем, что задача была удалена
    response = await async_client.get(f"/tasks/tasks/{task.id}")
    assert response.status_code == 404
