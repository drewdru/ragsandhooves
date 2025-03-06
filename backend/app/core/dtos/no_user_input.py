from pydantic import BaseModel
from typing import Any

from app.core.services.agents.agent_abstraction import AgentClient

class NoUserInput(BaseModel):
    client: AgentClient
    parameters: Any