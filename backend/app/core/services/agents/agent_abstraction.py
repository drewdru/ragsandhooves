from pydantic import BaseModel
from abc import ABC, abstractmethod

class AgentClient(BaseModel):
    pass


class InvokeParameters(BaseModel):
    client: AgentClient
    client_parameters: dict


class AgentResponse(BaseModel):
    pass


class Agent(ABC):
    @abstractmethod
    @staticmethod
    def setup_client () -> AgentClient:
        pass

    @abstractmethod
    @staticmethod
    def invoke(invoke_parameters: InvokeParameters) -> AgentResponse:
        pass