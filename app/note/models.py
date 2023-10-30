from sqlalchemy import Column, Integer, ForeignKey, DateTime,Boolean,String
from sqlalchemy.orm import relationship
from app.db import Base
from app.user.models import User

class Note(Base):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    note_body = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="notes")

    def __repr__(self):
        return f'Note(id={self.id}, title={self.title}, note_body={self.note_body})'