# api/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Query

from database.session import get_db
from models.user import User
from schemas.user import UserRead, UserCreate
from response.result import Result

router = APIRouter()

@router.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.post("/new/")
async def post_users_value(item: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/get_value/")
def get_value(name: str = Query(...), email: str = Query(...)):
    1/0
    return Result(200, "success", {"name": name, "email": email}).http_response()
