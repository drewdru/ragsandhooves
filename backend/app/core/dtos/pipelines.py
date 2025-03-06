from pydantic import BaseModel
from enum import Enum, auto

class PiplinesNames(str, Enum):
    GENERAL_Questing_Answering = "GENERAL_QA"
    DOCUMENTS_PARSING = "DOCUMENTS_PARSING"


