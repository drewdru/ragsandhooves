from enum import Enum, auto
from pydantic import BaseModel
from .knowledge_bases import KnowledgeBase
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
import uuid

from app.core.dtos.pipelines import PiplinesNames
from app.core.dtos.agents import Agents, NoUserInput


class PipelineAgentConfigurations(SQLModel, table=True):
    __tablename__ = "pipeline_agent_configurations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    description: str | None = Field(default=None, max_length=255)
    pipeline_name: PiplinesNames = Field(default=None)

    knowledge_base: uuid.UUID = Field(default_factory=uuid.uuid4)
    agent_name: Agents = Field(default=None)
    agent_parameters: dict = Field(sa_type=JSONB, nullable=False) 