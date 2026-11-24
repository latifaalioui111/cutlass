# Cutlass

Deliberately vulnerable application, for educational use only.
Never expose outside a local lab (kind).


Cutlass simulates attack scenarios against a small Kubernetes
application, acting as the offensive counterpart to an automated
detection-and-response system.

## Disclaimer

Built for security research and learning purposes. Only run this
against your own local lab. The authors take no responsibility for
any misuse.

## License

MIT

## Architecture

- `target-app/`: a deliberately vulnerable FastAPI application
  (command injection via `/ping`).
- `attacker/`: the attack engine. Each step is a Strategy
  (`steps/*.py`), run through a shared Template Method (`steps/base.py`),
  built from a YAML scenario file via a Factory (`step_factory.py`).
  Progress is broadcast live over WebSocket (Observer pattern).

## Running the demo

1. `kind create cluster --name cutlass-lab`
2. `kubectl apply -f k8s/target.yaml`
3. `kubectl -n lab port-forward svc/target-app 8000:80`
4. `cd attacker && python3 run_scenario.py`
5. Open `http://localhost:8080` to watch the live console.

## Threat model

An attacker with network access to the target application exploits
a command injection vulnerability to gain code execution, reads a
simulated Kubernetes ServiceAccount token, and exfiltrates it —
following MITRE ATT&CK techniques T1059, T1082, T1552 and T1041.
