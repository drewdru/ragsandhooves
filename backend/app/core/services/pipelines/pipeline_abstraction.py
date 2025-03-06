from typing import Any, Callable, Dict, TypeVar, Generic, Union
from pydantic import BaseModel
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from requests import Response
import logging

from app.core.services.agents_pipeline.agent_pipeline_abstraction import AgentPipline
from app.core.dtos.agents import Agents
from app.core.dtos.no_user_input import NoUserInput


# Define types for better clarity
T = TypeVar('T')
Context = Dict[str, Any]

class PipelineStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    PROCESSING = auto()


class IntementsTupes(Enum):
    NON_USER_INPUT = auto()
    USER_INPUT = auto()


class ContextInctement(BaseModel):
    type: IntementsTupes | None = None
    agent_name: Agents | None = None
    increment_name: str | None = None
    data: Any | None = None 

class PiplineData(BaseModel):
    class Config:
        extra = "allow"


class PipelineContext(BaseModel):
    data: PiplineData = PiplineData()
    created_at: datetime = datetime.now()
    status: PipelineStatus = PipelineStatus.PROCESSING
    # error: Exception | None = None

    @staticmethod
    def _build_key(increment:ContextInctement) -> str:
        data_valudation = (
            increment.type == IntementsTupes.USER_INPUT, 
            increment.agent_name is not None,
            increment.increment_name is not None,
        )

        match data_valudation:
            case (False, False, True):
                key = increment.increment_name
            case (True, False, False):
                key = increment.type.value
            case (False, True, False):
                key = f"{increment.agent_name.name}_{increment.type.name}"
            case _:
                raise ValueError(f"Invalid increment data")

        return key

    def update(self, new_data:ContextInctement) -> None:
        key = self._build_key(new_data)
        data = new_data.data
        setattr(self.data, key, data)

    def get (self, requested_data:ContextInctement) -> Any:
        key = self._build_key(requested_data)
        print (f"get key is {key}")
        return getattr(self.data, key)


class PipelineResult(Generic[T]):
    success: bool
    data: Dict[str, Any]
    error: Exception | None = None


class Pipeline:
    def __init__(
            self, 
            user_input: Dict[str, Any], 
            steps: list[AgentPipline],
            logger: logging.Logger | None = None
        ):
        self.user_input: Dict[str, Any] = user_input
        self.steps: list[AgentPipline] = steps
        self.context = PipelineContext()
        self.logger = logger or logging.getLogger(__name__)

    def userimput_to_context(self) -> None:
        """
        Purpose:
            Add user input to context;
        """
        _context_increment = ContextInctement(
            type=IntementsTupes.USER_INPUT,
            agent_name=None,
            increment_name=None,
            data=self.user_input
        )
        self.context.update(_context_increment)

        self.logger.info(f"User input added to context")

    def nouserimput_to_context(self) -> None:
        """
        Purpose:
            For all steps in the pipline we:
                Iniciate AgentPipline.non_user_input dataobject
                Setup client and save them to AgentPipline.non_user_input.client;
                Upload non_user_input and save them to AgentPipline.non_user_input.client_parameters from database
        """
        
        for agent in self.steps:
            _no_user_input: NoUserInput = agent.no_user_input
            _no_user_input.client = agent.setup_client()
            _no_user_input.parameters = self._upload_non_user_settings()
            _context_increment = ContextInctement(
                type=IntementsTupes.NON_USER_INPUT,
                agent_name=agent.agent_name,
                increment_name=None, #For Non user input we do not need increment name
                data=_no_user_input
            )
            self.context.update(_context_increment)
            self.logger.info(f"Non user input added to context for {agent.agent_name}")

        self.logger.info(f"Non user input added to context for all agents")

    def _upload_non_user_settings(self) -> dict:
        """
        Purpose:
            Upload non_user_settings from database
        """
        pass

    def execute(self) -> PipelineContext:
        """Execute all pipeline steps in order"""
        for func, input_mapping in self.steps:
            try:
                # Prepare input parameters from context
                params = {
                    param_name: self.context.get(context_key)
                    for param_name, context_key in input_mapping.items()
                }
                
                # Execute the function (already wrapped if needed)
                result = func(**params)
                
                # Update context with results
                self.context.update(result)
                
            except Exception as e:
                self.logger.error(f"Step failed: {func.__name__}", exc_info=True)
                self.context.status = PipelineStatus.FAILURE
                self.context.error = e
                break
        
        if self.context.status == PipelineStatus.PENDING:
            self.context.status = PipelineStatus.SUCCESS
            
        return self.context
