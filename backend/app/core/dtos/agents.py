from enum import Enum, auto
from pydantic import BaseModel

class NoUserInput(BaseModel):
    data: str
    pass

class InvokeParameters(BaseModel):
    pass

class ContextDependedInput(BaseModel):
    pass

class AgentPropertyes(BaseModel):
    no_user_input: NoUserInput
    invoke_parameters: InvokeParameters
    context_dependent_input: ContextDependedInput


class Agents(Enum):
    pass
    # GEMINI_ANSWER_EXTRACTOR = AgentPropertyes(
    #     no_user_input=auto(), # MUST BE specific agent realisation
    #     invoke_parameters=auto(), # MUST BE specific agent realisation
    #     context_dependent_input=auto(), # MUST BE specific agent realisation
    # )
