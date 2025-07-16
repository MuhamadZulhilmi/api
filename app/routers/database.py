from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.db.database import get_db

router = APIRouter(
    prefix="/database",
    tags=["database"]
)

@router.get("/db")
def get_db_tables(db: Session = Depends(get_db)):
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    return {"tables": tables}
