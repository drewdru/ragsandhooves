from pydantic import BaseModel
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, text

from app.core.services.agents.agent_abstraction import Agent, AgentResponse, InvokeParameters
from app.core.dtos.agents import Agents



class MapObject(BaseModel):
    source: str
    target: str

class AgentPipline(ABC, Agent):
    def __init__(self, agent: Agents):
        self.agent: Agents
        self.map_context_dependencies: list[MapObject]
        self.map_response_to_context: list[MapObject]

    @abstractmethod
    def build_invoke_parameters(self) -> InvokeParameters:
        """
        Purpose:
            Map data FROM self.agent.context_dependency & self.agent.no_user_input 
                     TO self.agent.invoke_parameters
        """
        pass

    @abstractmethod
    def postprocess_response(self) -> AgentResponse:
        """
        Purpose:
            Postprocess object that function self.invoke return 
            to a something that can be utilized to in pipeline.
        """
        pass
    
    def invoke_pipline_agent(
        self, 
    ) -> AgentResponse:
        invoke_parameters = self.build_invoke_parameters()
        raw_response = self.invoke(**invoke_parameters)
        return self.postprocess_response(raw_response)