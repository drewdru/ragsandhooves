from abc import ABC, abstractmethod
from typing import Any

class DocumentProvider(ABC):
    client: Any  # Declare that the client attribute should exist in the subclass
    
    @abstractmethod
    def __init__(self):
        """Initialize the client"""
        pass

    @abstractmethod
    def download(self, file_info: dict, temp_path: str) -> None:
        """Download file and returns bytes"""
        pass
