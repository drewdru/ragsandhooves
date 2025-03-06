from abc import ABC, abstractmethod
from dataclasses import dataclass, 
from typing import TypeVar, Dict, Any
from enum import Enum, auto
from pydantic import BaseModel, ConfigDict


class Agents(Enum):
    GEMINI_ANSWER_EXTRACTOR = auto()
    MISTRAL_ANSWER_EXTRACTOR = auto()
    COHERE_RERANKER = auto()


@dataclass
class AgentClient:
    agent_client: Any


@dataclass
class AgentResponse:
    response: Any


@dataclass
class InvokeParameters:
    parameters: Dict[str, Any]


@dataclass
class NoUserSettings:
    agent_type: Agents


@dataclass
class ContextObjext:
    context: Dict[str, Any]


@dataclass
class PipelineObject:
    key: str
    value: Any

@dataclass
class PipelineContext:
    model_config = ConfigDict(extra='allow')

    def update(self, new_record: PipelineObject) -> None:
        setattr(self, new_record.key, new_record.value)


class Agent (ABC):
    agent_type: Agents
    no_user_settings: NoUserSettings
    invoke_parameters: InvokeParameters

    @abstractmethod
    @staticmethod
    def setup_client() -> AgentClient:
        pass
    
    @abstractmethod
    def invoke(self, Agent) -> AgentResponse:
        pass
    
    @abstractmethod
    def build_invoke_parameters(self) -> InvokeParameters:
        """
        Propose: 
            We have a some universal NoUserSettings that
            configyrate some constant parameters like prompt, temperature, etc.
            Use this method to map NoUserSettings to InvokeParameters.
        """
        pass


class PipelineAgent(ABC, Agent):
    """
    Purpose: 
        Adopt the Agent interface for using in a pipeline
        We use 2 methods for that:
            - extract_parameters_from_context:
                Extract parameters from context and map them to invoke_parameters.
                So, as a result we have fully prepared parameters for invoking.
            - postprocess_response
                Make the response usable for the next pipeline steps or be a pipeline's final result. 
    """
    def __init__(self, context: PipelineContext) -> None:
        self.context = context

    @abstractmethod
    def extract_parameters_from_context (self) -> None:
        pass

    @abstractmethod
    def postprocess_response(self, AgentResponse) -> ContextObjext:
        pass

