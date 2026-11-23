"""
WebSocket server: broadcasts scenario events to every connected
browser in real time. This is the Observer that the console listens to.
"""
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Cutlass Live Console")

connected_clients: list[WebSocket] = []

# Will hold a reference to the event loop running in the server thread,
# so broadcast_sync (called from the main thread) can reach it.
server_loop: asyncio.AbstractEventLoop | None = None


@app.on_event("startup")
async def capture_loop():
    """Called once, right when Uvicorn's event loop starts.
    We grab a reference to it here so other threads can use it later."""
    global server_loop
    server_loop = asyncio.get_running_loop()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def broadcast(event: dict):
    message = json.dumps(event)
    for client in connected_clients:
        await client.send_text(message)


def broadcast_sync(event: dict):
    """Bridge: called synchronously from the main thread (by
    ScenarioRunner), but broadcasting is async and lives on the
    server thread's event loop. run_coroutine_threadsafe schedules
    it there safely, across threads."""
    if server_loop is not None:
        asyncio.run_coroutine_threadsafe(broadcast(event), server_loop)


@app.get("/")
def console():
    return HTMLResponse(open("console.html").read())
