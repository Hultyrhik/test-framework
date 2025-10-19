from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTestAdapter(ABC):
    @abstractmethod
    def run(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        pass