
from engine.runtime.session import Session


def leave_character_context(session: Session):
    session.character = None
    session.ctx.router.unregister(session.id)
