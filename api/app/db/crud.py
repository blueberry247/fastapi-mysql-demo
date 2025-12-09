from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import Item, ItemCreate


def create_item(db: Session, item_in: ItemCreate) -> Item:
    item = Item(name=item_in.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_items(db: Session) -> List[Item]:
    return db.query(Item).all()


def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()


def delete_item(db: Session, item_id: int) -> bool:
    item = get_item(db, item_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

