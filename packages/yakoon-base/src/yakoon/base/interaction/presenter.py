from typing import Protocol


class Prompts(Protocol):

    async def ask(self, section: str, **data) -> str: ...
    """     
    Asks the user for free-text input based on a rendered template section.

    Args:
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        str: The user's input as a string.
    """

    async def confirm(self, section: str, **data) -> bool: ...
    """
    Asks the user for a yes/no confirmation using a template-based prompt.

    Args:
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        bool: True if confirmed, False otherwise.
    """

    async def choice(self, section: str, options: list[str], **data) -> str: ...
    """
    Presents the user with a list of choices and returns the selected value.

    Args:
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        str: The chosen value.
    """        

    async def choice_index(self, section: str, options: list[str], **data) -> str: ...
    """
    Presents the user with a numbered list of choices and returns the selected index.

    Args:
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        int: The index of the selected choice (starting at 0).
    """
 

class Presenter(Protocol):

    prompts: Prompts

    async def emit(self, section: str, **data) -> None: ...
    """
    Renders and emits a section of the current template via session.emit().

    Used for standard informational output (e.g. success, details, confirmations).

    Args:
        section (str): Template section key (e.g. "success", "info").
        **data: Optional key-value pairs for template variables.
    """

    async def fail(self, section: str, **data) -> None: ...
    """
    Renders and sends a failure message via session.fail().

    Used to communicate errors, invalid inputs, or blocked operations.

    Args:
        section (str): Template section key (e.g. "not_found", "denied").
        **data: Optional key-value pairs for template variables.
    """

    async def notify(self, section: str, **data) -> None: ...
    """
    Renders and sends a passive notification via session.notify().

    Used for non-critical messages, hints or background updates.

    Args:
        section (str): Template section key (e.g. "hint", "auto_saved").
        **data: Optional key-value pairs for template variables.
    """