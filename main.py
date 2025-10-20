from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# создан экземпляр класса
app = FastAPI(
    title='py_hub_api',
    description='Platform',
    version='1.0.0'
)
# запуск серввера python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
# http://localhost:8000/docs
# http://127.0.0.1:8000/docs

# Модели данных в pydentic
class UserBase(BaseModel):
    username: str
    email: str


class UserCrate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode: True


class CourseBase(BaseModel):
    title: str
    description: str
    price: float = 0.0


class CourseResponse(CourseBase):
    id: int
    created_at: datetime


# Временное хранилище
users_db = []
courses_db = []


# endpoints
@app.get("/")
async def root():
    return {
        'message': 'Hello',
        'version': '1.0.0',
        'docs': '/docs'
    }


@app.get("/health")
async def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now()
    }


@app.post("/users/", response_model=UserResponse)
async def created_user(user: UserCrate):
    user_date = user.dict()
    user_date["id"] = len(users_db) + 1
    user_date["created_at"] = datetime.now()
    users_db.append(user_date)
    return user_date

@app.get("/users/{id}/", response_model=UserResponse)
async def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return {"error": "User not found"}
    return user


@app.post("/courses/", response_model=CourseResponse)
async def created_courses(course: CourseBase):
    course_date = course.dict()
    course_date["id"] = len(courses_db) + 1
    course_date["created_at"] = datetime.now()
    courses_db.append(course_date)
    return course_date


@app.get("/courses/", response_model=list[CourseResponse])
async def get_courses():
    return courses_db
