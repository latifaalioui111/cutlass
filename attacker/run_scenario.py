import threading
import time
import uvicorn
import yaml
from scenario_runner import ScenarioRunner
from ws_server import app, broadcast_sync

with open("scenarios/default.yaml") as f:
    config = yaml.safe_load(f)


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    # Start the WebSocket server in a background thread so the
    # attack scenario can run in the main thread at the same time.
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # give the server a moment to start

    print("Open http://localhost:8080 in your browser, then press Enter.")
    input()

    runner = ScenarioRunner(config["steps"], observers=[broadcast_sync])
    runner.run()
