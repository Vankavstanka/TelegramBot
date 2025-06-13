from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, Base, get_session
import models, schemas

app = FastAPI(title="Tasks API")

# запуск БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
app = FastAPI(title="Tasks API", lifespan=lifespan)

# эндпойнты
@app.get("/tasks", response_model=list[schemas.TaskRead])
async def list_tasks(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Task))
    return result.scalars().all()

@app.post("/tasks", response_model=schemas.TaskRead)
async def add_task(task: schemas.TaskCreate, session: AsyncSession = Depends(get_session)):
    db_task = models.Task(**task.dict())
    session.add(db_task)
    await session.commit()
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await session.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    await session.delete(task)
    await session.commit()
