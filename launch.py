from sqlalchemy.orm import Session

from app.models.meta import BaseModel
from app.utilities.database import engine


BaseModel.metadata.create_all(bind=engine)
