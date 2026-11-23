import time
from abc import ABC, abstractmethod


class AttackStep(ABC):
    """
    Base class (Template Method): defines the shared flow for every
    attack step. Each subclass only implements `execute()`; timing
    and output formatting are handled here.
    """

    name: str = "unnamed-step"
    mitre_id: str = "T0000"

    def run(self) -> dict:
        print(f"[{self.mitre_id}] {self.name}...")
        start = time.time()
        result = self.execute()
        duration = time.time() - start
        print(f"    -> {result.get('summary', '')} ({duration:.2f}s)")
        return {
            "name": self.name,
            "mitre_id": self.mitre_id,
            "duration": duration,
            **result,
        }

    @abstractmethod
    def execute(self) -> dict:
        """Each concrete step must return a dict with at least 'summary'."""
        ...
