from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from app import db
from . import services
from . schemas import TaskCreate,Task,TaskSchema,TaskUpdate,TaskBase
from app.auth.jwt import get_current_user
from app.user.schema import User

router = APIRouter(
    tags=['Tasks'],
    prefix='/api'
)

@router.post("/tasks/", response_model=Task)
async def create_task_api(task: TaskBase,current_user: User = Depends(get_current_user),database: Session = Depends(db.get_db)):
    create_task = await services.create_task(task,database,current_user.id)
    return create_task

@router.get('/tasks/',response_model=List[Task])
async def get_tasks(current_user: User = Depends(get_current_user),database: Session = Depends(db.get_db)):
   return await services.fetch_tasks_lists(current_user.id,database)

@router.get('/tasks/{task_id}',response_model=Task)
async def get_task_by_id(task_id: int,current_user: User = Depends(get_current_user),database: Session = Depends(db.get_db)):
    return await services.get_task(task_id,current_user.id,database)
# #creating Task
# @app.post("/tasks/", response_model=Task,tags=["Tasks"])
# def create_task_api(task: TaskCreate, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
#     return create_task(db, task, current_user.id)

# #Users Task per owner id
# @app.get("/tasks/", response_model=List[Task],tags=["Tasks"])
# def get_tasks_api(current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
#     tasks = get_tasks(db, current_user.id)
#     return tasks

# def get_task(db: SessionLocal, task_id: int):
#     task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     return task

@router.delete("/tasks/{task_id}", response_model=TaskSchema,tags=["Tasks"])
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    # Check if the task exists and belongs to the current user
    task = await services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Delete the task
    database.delete(task)
    database.commit()

    return task


@router.put("/tasks/{task_id}", response_model=Task,tags=["Tasks"])
async def update_task(task_id: int, task_data: TaskUpdate, current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    # Check if the task exists and belongs to the current user
    task = await services.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Update the task's properties
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    # Commit the changes to the database
    database.commit()

    return task