#import required moules as usuals
from typing import Optional

from sqlalchemy.orm import Session

from .models import User

#verifyif the email already exist in the database 
async def verify_email_exist(email: str, db_session: Session) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()