import uuid

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from app.core.models.recognition_results import RecognitionResult


class RecognitionResultsMetadata(SQLModel, table=True):
    __tablename__ = "recognition_results_metadata"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    text: str | None
    summary: str | None
    
    meta: dict = Field(sa_type=JSONB, nullable=False)

    recognition_result: Optional["RecognitionResult"] = Relationship(
        sa_relationship_kwargs={'uselist': False, 'single_parent': True},
        back_populates="recognition_result_metadata"
    )