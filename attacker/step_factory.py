"""
Factory: turns a plain text name into a concrete step instance.
Lets a scenario be described as a simple list of names, without
writing Python code for every possible combination.
"""
from steps.injection import InjectionStep
from steps.discovery import DiscoveryStep
from steps.credential_access import CredentialAccessStep
from steps.exfiltration import ExfiltrationStep

TARGET_URL = "http://localhost:8000"

_last_token = {"value": "unknown"}  # simple memory between steps


def create_step(step_name: str):
    if step_name == "injection":
        return InjectionStep(TARGET_URL)
    elif step_name == "discovery":
        return DiscoveryStep(TARGET_URL)
    elif step_name == "credential_access":
        return CredentialAccessStep()
    elif step_name == "exfiltration":
        return ExfiltrationStep(token=_last_token["value"])
    else:
        raise ValueError(f"Unknown step: {step_name}")


def remember_token(result: dict):
    """If the step produced a token, keep it for the next step."""
    if "token" in result:
        _last_token["value"] = result["token"]
