import asyncio

class DialogManager:
    def __init__(self):
        self._waiting = {}  # session_id → Future

    def is_waiting(self, session_id):
        return session_id in self._waiting

    def set_prompt(self, session):
        fut = asyncio.get_event_loop().create_future()
        self._waiting[session.id] = fut
        return fut

    def resolve(self, session_id, value):
        fut = self._waiting.pop(session_id, None)
        if fut and not fut.done():
            fut.set_result(value)

    @staticmethod
    def is_waiting_to_handle(session_id, input_str:str):
        if dialog_manager.is_waiting(session_id):
            dialog_manager.resolve(session_id, input_str)
            return True

dialog_manager = DialogManager()



