from step_factory import create_step, remember_token


class ScenarioRunner:

    """Chains a list of steps, collects their results, and notifies observers (callbacks) after each step completes."""

    def __init__(self, step_names: list[str], observers: list = None):
        self.step_names = step_names
        self.results = []
        self.observers = observers or []

    def _notify(self, event: dict):
        """Call every registered observer with the event data.
        Each observer decides what to do with it (print, broadcast, save...)."""
        for observer in self.observers:
            observer(event)

    def run(self) -> list[dict]:
        self._notify({"type": "scenario_started", "steps": self.step_names})
        for step_name in self.step_names:
            step = create_step(step_name)
            result = step.run()
            remember_token(result)
            self.results.append(result)
            self._notify({"type": "step_completed", **result})
        total = sum(r["duration"] for r in self.results)
        self._notify({"type": "scenario_finished", "total_duration": total})
        return self.results
