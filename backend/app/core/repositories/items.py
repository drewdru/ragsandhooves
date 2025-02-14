import uuid
from sqlmodel import Session

from app.core.models.items import Item
from app.core.dtos.items import ItemCreate 


class ItemsRepository:
    """Encapsulates all items-related database operations."""

    @staticmethod
    def create_item(session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
        db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    
    @staticmethod
    def get_item_by_id(
        session: Session,
        id: uuid.UUID,
    ) -> Item:
        return session.get(Item, id)
