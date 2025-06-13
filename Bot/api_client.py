import httpx
from config import get_settings

settings = get_settings()
BASE = str(settings.API_URL)

async def get_tasks() -> list[dict]:
    async with httpx.AsyncClient(base_url=BASE) as client:
        resp = await client.get("/tasks")
        resp.raise_for_status()
        return resp.json()

async def add_task(name: str, deadline: str) -> dict:
    async with httpx.AsyncClient(base_url=BASE) as client:
        resp = await client.post("/tasks", json={"name": name, "deadline": deadline})
        resp.raise_for_status()
        return resp.json()

async def delete_task(task_id: int):
    async with httpx.AsyncClient(base_url=BASE) as client:
        resp = await client.delete(f"/tasks/{task_id}")
        resp.raise_for_status()
