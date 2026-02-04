
from yakoon.base.runtime.session.session import Session


def format_prompt(session: Session, 
                  default_prompt="shell", 
                  active_controller="shell") -> str:
    """
    Formats the interactive prompt based on session state.

    Examples:
      - shell$
      - stefan@shell$
      - stefan@auth$
    """
    if not session:
        return default_prompt

    user = session.get_username()
    controller = session.get_active_controller(active_controller)

    if user:
        return f"{user}@{controller}$ "
    return f"{controller}$ "
