from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    name: str
    deadline: str

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    name: str
    deadline: str
