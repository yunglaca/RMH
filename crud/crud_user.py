from utils.user import get_user_from_db, create_user_in_db
from fastapi import APIRouter, status
from schemas.schemas import UserCreate
from DB.database import db_dependency

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = await get_user_from_db(db, user_id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, db: db_dependency):
    user = await create_user_in_db(db, user_create)

    return {"message": "User created successfully", "user": user}
