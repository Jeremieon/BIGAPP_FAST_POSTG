from typing import List
from app import db
from app.tasks.models import TaskDB
from . import models

async def create_task(task,database) -> models.TaskDB:
    db_task = TaskDB(**task.dict())
    database.add(db_task)
    database.commit()
    database.refresh(db_task)
    return db_task

async def fetch_tasks_lists(database) -> List[models.User]:
   return database.query(models.TaskDB).all()

async def get_task(database,task_id):
    task = database.query(TaskDB).filter(TaskDB.id == task_id).first()
    return task