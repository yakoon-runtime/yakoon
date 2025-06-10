import os

class LoopSettings:
    tenant: str = os.getenv("YAKOON_TENANT", "acme")
    controller_id: str = os.getenv("YAKOON_CONTROLLER_ID", "realm")
    token: str = os.getenv("YAKOON_TOKEN", "dev-token")
    url: str = os.getenv("YAKOON_LOOP_URL", "ws://127.0.0.1:8000/ws/loop")
