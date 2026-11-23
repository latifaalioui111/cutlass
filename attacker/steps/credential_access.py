from .base import AttackStep


class CredentialAccessStep(AttackStep):
    name = "Read a simulated token"
    mitre_id = "T1552"

    def execute(self) -> dict:
        fake_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImZha2Uta2V5LWlkIn0.FAKE.TOKEN"
        return {"summary": f"token found: {fake_token[:20]}...", "token": fake_token}
