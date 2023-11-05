from typing import List
from app import db
from app.tasks.models import TaskDB
from . import models
from app.auth.jwt import get_current_user
from app.user.models import User

async def create_task(task,database,owner_id:int) -> models.TaskDB:
    db_task = TaskDB(**task.dict(),owner_id=owner_id)
    database.add(db_task)
    database.commit()
    database.refresh(db_task)
    return db_task

async def fetch_tasks_lists(owner_id:int,database) -> List[models.User]:
   return database.query(TaskDB).filter(TaskDB.owner_id==owner_id).all()

async def get_task(task_id,owner_id:int,database):
    task = database.query(TaskDB).filter(TaskDB.owner_id==owner_id).filter(TaskDB.id == task_id).first()
    return task