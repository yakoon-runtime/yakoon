from dataclasses import dataclass

@dataclass
class CommandRequest:
    command: str
    args: dict
    session_id: str
    tenant: str
    controller: str
    trace_id: str

@dataclass
class CommandResponse:
    success: bool
    result: dict
    error: str | None = None
