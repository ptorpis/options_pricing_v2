from abc import ABC, abstractmethod

class AbstractModel(ABC):
    @abstractmethod
    def build(self):
        """Build and return the QuantLib process or model."""
        pass
