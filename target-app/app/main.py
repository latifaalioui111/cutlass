import subprocess
from fastapi import FastAPI

app = FastAPI(title="Target App (DELIBERATELY VULNERABLE - lab only)")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products")
def products():
    return [{"id": 1, "name": "Keyboard"}, {"id": 2, "name": "Mouse"}]


# Intentional vulnerability: command injection.
# `shell=True` runs the string through a shell (bash/sh), so any shell
# special character (;, &&, |) the user slips into `host` gets
# interpreted, not just passed to `ping`.
@app.get("/ping")
def ping(host: str):
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return {"stdout": result.stdout, "stderr": result.stderr}
