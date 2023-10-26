from typing import Optional

from sqlalchemy.orm import Session

from .models import Categories


async def verify_category_exist(category_id: int, db_session: Session) -> Optional[Categories]:
    return db_session.query(Categories).filter(Categories.id == category_id).first()