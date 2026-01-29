from yakoon.base.runtime.views.context import RenderContext
from yakoon.base.runtime.dialogs.prompts import ask, choice, choice_index, confirm
from yakoon.base.runtime.session import Session


class Prompts:
    """
    Provides interactive input methods for user sessions using localized templates.

    This class encapsulates all prompt-based interactions such as text input,
    confirmations, and choices. 
    """

    def __init__(self, ctx: RenderContext, session: Session, renderer: "RendererService"):
        self._ctx = ctx
        self._session = session
        self._renderer = renderer

    async def ask(self, section: str, **data) -> str:
        """     
        Asks the user for free-text input based on a rendered template section.

        Args:
            section (str): The section key within the template.
            **data: Optional data passed to the template.

        Returns:
            str: The user's input as a string.
        """
        question = await self._renderer.render(self._ctx, section, **data)
        return await ask(self._session, question)

    async def confirm(self, section: str, **data) -> bool:
        """
        Asks the user for a yes/no confirmation using a template-based prompt.

        Args:
            section (str): The section key within the template.
            **data: Optional data passed to the template.

        Returns:
            bool: True if confirmed, False otherwise.
        """
        question = await self._renderer.render(self._ctx, section, **data)
        return await confirm(self._session, question, **data)

    async def choice(self, section: str, options: list[str], **data) -> str:
        """
        Presents the user with a list of choices and returns the selected value.

        Args:
            section (str): The section key within the template.
            choices (list[str]): List of available options.
            **data: Optional data passed to the template.

        Returns:
            str: The chosen value.
        """        
        question = await self._renderer.render(self._ctx, section, **data)
        return await choice(self._session, question, options)

    async def choice_index(self, section: str, options: list[str], **data) -> str:
        """
        Presents the user with a numbered list of choices and returns the selected index.

        Args:
            section (str): The section key within the template.
            choices (list[str]): List of available options.
            **data: Optional data passed to the template.

        Returns:
            int: The index of the selected choice (starting at 0).
        """
        question = await self._renderer.render(self._ctx, section, **data)
        return await choice_index(self._session, question, options)
