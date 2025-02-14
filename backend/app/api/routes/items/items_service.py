import uuid
from typing import Any

from app.core.models.users import User
from app.core.repositories.items import ItemsRepository
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, func, select

from app.core.models.items import Item
from app.core.dtos.items import ItemCreate, ItemsPublic, ItemUpdate
from app.core.dtos.message import Message

router = APIRouter(prefix="/items", tags=["items"])

class ItemsValidationService:
    @staticmethod
    def check_current_user_permissions(item: Item, current_user: User):
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if not current_user.is_superuser and (item.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")

class ItemsService:
    """Handles items-related business logic and database operations"""

    @staticmethod
    def read_items(
        session: Session, current_user: User, skip: int = 0, limit: int = 100
    ) -> Any:
        """
        Retrieve items.
        """
        if current_user.is_superuser:
            count_statement = select(func.count()).select_from(Item)
            count = session.exec(count_statement).one()
            statement = select(Item).offset(skip).limit(limit)
            items = session.exec(statement).all()
        else:
            count_statement = (
                select(func.count())
                .select_from(Item)
                .where(Item.owner_id == current_user.id)
            )
            count = session.exec(count_statement).one()
            statement = (
                select(Item)
                .where(Item.owner_id == current_user.id)
                .offset(skip)
                .limit(limit)
            )
            items = session.exec(statement).all()
        return ItemsPublic(data=items, count=count)

    @staticmethod
    def read_item(session: Session, current_user: User, id: uuid.UUID) -> Any:
        """
        Get item by ID.
        """
        item = ItemsRepository.get_item_by_id(
            session, current_user, id,
        )
        ItemsValidationService.check_current_user_permissions(item, current_user)
        return item

    @staticmethod
    def create_item(
        session: Session, current_user: User, item_in: ItemCreate
    ) -> Any:
        """
        Create new item.
        """
        item = Item.model_validate(item_in, update={"owner_id": current_user.id})
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    @staticmethod
    def update_item(
        session: Session,
        current_user: User,
        id: uuid.UUID,
        item_in: ItemUpdate,
    ) -> Any:
        """
        Update an item.
        """
        item: Item = ItemsRepository.get_item_by_id(
            session, current_user, id,
        )
        ItemsValidationService.check_current_user_permissions(item, current_user)
        update_dict = item_in.model_dump(exclude_unset=True)
        item.sqlmodel_update(update_dict)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


    @staticmethod
    def delete_item(
        session: Session, current_user: User, id: uuid.UUID
    ) -> Message:
        """
        Delete an item.
        """
        item = ItemsRepository.get_item_by_id(
            session, current_user, id,
        )
        ItemsValidationService.check_current_user_permissions(item, current_user)
        session.delete(item)
        session.commit()
        return Message(message="Item deleted successfully")
