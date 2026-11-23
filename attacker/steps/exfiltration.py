from .base import AttackStep


class ExfiltrationStep(AttackStep):
    name = "Simulated exfiltration"
    mitre_id = "T1041"

    def __init__(self, token: str = "unknown"):
        self.token = token

    def execute(self) -> dict:
        with open("exfiltrated.txt", "a") as f:
            f.write(f"stolen token: {self.token}\n")
        return {"summary": "data written to exfiltrated.txt"}
