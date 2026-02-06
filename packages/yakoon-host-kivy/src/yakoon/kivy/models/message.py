from dataclasses import dataclass

@dataclass
class Message:
    text: str
    role: str = "system"   # user | system | output
