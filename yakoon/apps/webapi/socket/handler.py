import uuid
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from yakoon.engine.core.dialog.manager import DialogManager
from yakoon.engine.runtime import Engine
from yakoon.platform.render.render_mode import RenderMode
from yakoon.solution.platform.registry import SolutionRegistry
from yakoon.solution.settings import SolutionSettings

# Set the global rendering mode to ansi text (no Markdown formatting)
SolutionSettings.runtime.render_mode = RenderMode.MARKDOWN

engine = Engine(SolutionRegistry())

router = APIRouter()
active_sessions = {}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    session_id = f"ws-{uuid.uuid4().hex[:6]}"

    print(f"[WebSocket] Connected: {session_id}")

    async def out(msg: str):
        await websocket.send_text(msg)

    async def err(msg: str):
        await websocket.send_text(f"⚠️ {msg}")

    try:
        await engine.signal_ready(out)
        while True:               
            await asyncio.sleep(0.1)
            data = await websocket.receive_text()              

            await engine.send(session_id, data, out, err)

    except WebSocketDisconnect:
        print(f"[WebSocket] Disconnected: {session_id}")
        # hier ggf. cleanup z. B. session schließen
