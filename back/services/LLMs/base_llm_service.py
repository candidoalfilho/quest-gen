from abc import ABC, abstractmethod

class BaseLLM(ABC):
    
    @abstractmethod
    def _configure_client(self):
        pass

    @abstractmethod
    def generate_response(self):
        pass
