##### DRAFT #####

class Prompts ():
    id: uuid
    agent: enum 
    description: str
    kb_id: uuid
    text: str = Field(default="my default prompt",)