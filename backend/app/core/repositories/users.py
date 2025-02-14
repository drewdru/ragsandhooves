from typing import Any
import uuid

from app.core.models.items import Item
from sqlmodel import Session, select, func, select, col, delete

from app.core.security import get_password_hash, verify_password
from app.core.models.users import User
from app.core.dtos.users import PrivateUserCreate, UserCreate, UserUpdate, UsersPublicPaginated

class UserRepository:
    """Encapsulates all user-related database operations."""

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        db_obj = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def create_private_user(session: Session, user_create: PrivateUserCreate) -> User:
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=get_password_hash(user_create.password),
        )
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def update_user(session: Session, db_user: User, user_in: UserUpdate) -> Any:
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        db_user.sqlmodel_update(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        session_user = session.exec(statement).first()
        return session_user
    
    @staticmethod
    def get_user_by_id(
        session: Session,
        user_id: uuid.UUID,
    ) -> User | None:
        return session.get(User, user_id)
    
    @staticmethod
    def get_paginated_users(session: Session, skip: int = 0, limit: int = 100) -> User | None:
        count_statement = select(func.count()).select_from(User)
        count = session.exec(count_statement).one()
        statement = select(User).offset(skip).limit(limit)
        users = session.exec(statement).all()
        return UsersPublicPaginated(data=users, count=count)


    @staticmethod
    def delete_user_by_id(
        session: Session,
        user: User,
    ) -> User | None:
        statement = delete(Item).where(col(Item.owner_id) == user.id)
        session.exec(statement)  # type: ignore
        session.delete(user)
        session.commit()

    @staticmethod
    def authenticate(session: Session, email: str, password: str) -> User | None:
        db_user = UserRepository.get_user_by_email(session=session, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user
