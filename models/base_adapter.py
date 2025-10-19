from abc import ABC, abstractmethod
from typing import Any

class BaseTestAdapter(ABC):
    @staticmethod
    @abstractmethod
    def run(test_data: dict[str, Any]) -> dict[str, Any]:
        pass