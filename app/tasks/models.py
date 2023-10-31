from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime,Boolean,String
from sqlalchemy.orm import relationship
from app.db import Base
from app.user.models import User


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    owner = relationship("User", back_populates="tasks")
