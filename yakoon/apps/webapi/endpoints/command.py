# yakoon/apps/webapi/endpoints/command.py

from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()

class CommandRequest(BaseModel):
    session_id: str
    input: str

@router.post("/run")
async def run_command(data: CommandRequest):
    # TODO: Dispatch command to Yakoon engine
    return {"status": "ok", "input": data.input}
