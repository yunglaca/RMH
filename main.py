import crud.crud_user as crud_user
import crud.crud_task as crud_task
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import UserCreate, UserResponse


app = FastAPI() 
app.include_router(crud_user.router)
app.include_router(crud_task.router)
