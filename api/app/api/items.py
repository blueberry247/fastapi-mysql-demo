from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.db.models import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[ItemRead])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item_in)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_item(db, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return

