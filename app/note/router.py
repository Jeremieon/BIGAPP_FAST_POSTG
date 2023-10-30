from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,status
from app.note import models
from app.auth.jwt import get_current_user
from sqlalchemy.orm.exc import UnmappedInstanceError
from app import db
from app.user.schema import User
from app.note.schema import NoteInput

router = APIRouter(
    tags=['Notes'],
    prefix='/api'
)

@router.get("/notes")
# current_user: User = Depends(get_current_user)
#filter(User.email == current_user.email)
def read_notes(database: Session = Depends(db.get_db)):
    try:
        notes = database.query(models.Note).all()
    finally:
        database.close()
    return notes

@router.get("/note/{note_id}")
def read_notes(note_id: int, database: Session = Depends(db.get_db)):
    try:
        note = database.query(models.Note).filter(models.Note.id == note_id).all()
    finally:
        database.close()
    return note

@router.post("/note")
def add_note(note: NoteInput,database: Session = Depends(db.get_db)):
    try:
        if len(note.title) == 0 and len (note.note_body) == 0:
            raise HTTPException(
                status_code=400, detail={
                     "status": "Error 400 - Bad Request",
                    "msg": "Both 'title' and 'note_body' are empty. These are optional attributes but at least one must be provided."
                }
            )
        new_note = models.Note(
            title=note.title, note_body=note.note_body
        )
        database.add(new_note)
        database.commit()
        database.refresh(new_note)
    finally:
        database.close()
    return new_note

@router.put("/note/{note_id}")
def update_note(note_id: int, updated_note: NoteInput,database: Session = Depends(db.get_db)):
    if len(updated_note.title) == 0 and len(updated_note.note_body) == 0:
        raise HTTPException(status_code=400, detail={
            "status": "Error 400 - Bad Request",
            "msg": "The note's `title` and `note_body` can't be both empty"
        })
    try:
        note = database.query(models.Note).filter(models.Note.id == note_id).first()
        note.title = updated_note.title
        note.note_body = updated_note.note_body
        database.commit()
        database.refresh(note)
    finally:
        database.close()
    return note

@router.delete("/note/{note_id}")
def delete_note(note_id: int,database: Session = Depends(db.get_db)):
    try:
        note = database.query(models.Note).filter(models.Note.id == note_id).first()
        database.delete(note)
        database.commit()
    except UnmappedInstanceError:
        raise HTTPException(status_code=400, detail={
            "status": "Error 400 - Bad Request",
            "msg": f"Note with `id`: `{note_id}` doesn't exist."
        })
    finally:
        database.close()
    return {
        "status": "200",
        "msg": "Note deleted successfully"
    }