# yakoon/apps/webapi/endpoints/command.py

from fastapi import APIRouter, Body
from pydantic import BaseModel

from yakoon.apps.webapi.session_manager import handle_input

router = APIRouter()

class CommandRequest(BaseModel):
    session_id: str
    input: str

@router.post("/run")
async def run_command(data: CommandRequest):
    result = await handle_input(data.session_id, data.input)
    return {"output": result}
