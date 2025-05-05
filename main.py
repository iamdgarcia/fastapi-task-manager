from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import uuid
from datetime import datetime

# Create FastAPI app instance
app = FastAPI(
    title="Task Manager API",
    description="A simple task management API built with FastAPI",
    version="1.0.0"
)

# Data Models
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# In-memory database
tasks_db = {}

# Helper functions
def get_task_or_404(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return tasks_db[task_id]

# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Task Manager API", 
        "docs": "/docs",
        "tasks_endpoint": "/tasks"
    }

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return list(tasks_db.values())

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    current_time = datetime.now()
    
    new_task = Task(
        id=task_id,
        created_at=current_time,
        updated_at=current_time,
        **task.dict()
    )
    
    tasks_db[task_id] = new_task
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    return get_task_or_404(task_id)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskCreate):
    task = get_task_or_404(task_id)
    
    task_data = task_update.dict()
    
    # Update task
    for key, value in task_data.items():
        setattr(task, key, value)
    
    task.updated_at = datetime.now()
    tasks_db[task_id] = task
    
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    get_task_or_404(task_id)  # Check if task exists
    del tasks_db[task_id]
    return None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
