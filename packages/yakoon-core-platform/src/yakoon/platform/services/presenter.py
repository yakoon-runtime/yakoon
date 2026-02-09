
from yakoon.base.models.prompt import PromptMode
from yakoon.base.ports import DialogService, RendererService
from yakoon.base.runtime.session import Session

from yakoon.base.directories.service import ServiceDirectory
from yakoon.platform.settings import settings
from yakoon.platform.runtime.render.context import RenderContext


class Prompts:
    """
    Provides interactive input methods for user sessions using localized templates.

    This class encapsulates all prompt-based interactions such as text input,
    confirmations, and choices. 
    """

    def __init__(self, ctx: RenderContext, 
                 session: Session, renderer: RendererService, dialogs: DialogService):
        self._ctx = ctx
        self._session = session
        self._renderer = renderer
        self._dialogs = dialogs

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
        return await ask(self._dialogs, self._session, question)
    
    async def ask_secret(self, section: str, **data) -> str:
        """     
        Asks the user for secret input based on a rendered template section.

        Args:
            section (str): The section key within the template.
            **data: Optional data passed to the template.

        Returns:
            str: The user's input as a string.
        """
        question = await self._renderer.render(self._ctx, section, **data)
        return await ask_secret(self._dialogs, self._session, question)

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
        return await confirm(self._dialogs, self._session, question, **data)

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
        return await choice(self._dialogs, self._session, question, options)

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
        return await choice_index(self._dialogs, self._session, question, options)


class Presenter:
    """
    Handles structured, localized output rendering for a command session.

    Wraps the template context and provides high-level methods for emitting
    messages, failures, and notifications using predefined sections in the template.
    """
    
    def __init__(self, template_prefix: str, template_key: str, 
                 session: Session, renderer: RendererService, dialogs: DialogService) -> RenderContext:
        """
        Constructs a RenderContext based on the current session and template key.

        Args:
            template_prefix (str): the template prefix
            template_key (str): Relative template path (e.g. 'account/cmd_login').
            session: Session object with language information.
            renderer: Renderservice to render the template. 

        Returns:
            RenderContext: Template context with full key and language.
        """
        self._prompts = None
        self._session = session
        self._renderer = renderer
        self._dialogs = dialogs
        
        self._ctx = RenderContext(
            key=template_key, prefix=template_prefix, 
            lang=session.lang, format=session.output_format)

    @property
    def prompts(self) -> Prompts:
        if not self._prompts:
            self._prompts = Prompts(
                self._ctx, self._session, 
                self._renderer, self._dialogs)
        return self._prompts

    async def emit(self, section: str, **data):
        """
        Renders and emits a section of the current template via session.emit().

        Used for standard informational output (e.g. success, details, confirmations).

        Args:
            section (str): Template section key (e.g. "success", "info").
            **data: Optional key-value pairs for template variables.
        """
        text = await self._renderer.render(self._ctx, section, **data)
        await self._session.emit(text)

    async def fail(self, section: str, **data):
        """
        Renders and sends a failure message via session.fail().

        Used to communicate errors, invalid inputs, or blocked operations.

        Args:
            section (str): Template section key (e.g. "not_found", "denied").
            **data: Optional key-value pairs for template variables.
        """
        text = await self._renderer.render(self._ctx, section, **data)
        await self._session.fail(text)

    async def notify(self, section: str, **data):
        """
        Renders and sends a passive notification via session.notify().

        Used for non-critical messages, hints or background updates.

        Args:
            section (str): Template section key (e.g. "hint", "auto_saved").
            **data: Optional key-value pairs for template variables.
        """
        text = await self._renderer.render(self._ctx, section, **data)
        await self._session.notify(text)


class PresenterService:

    def __init__(self, services: ServiceDirectory):
        self._services = services

    async def create_presenter(self, template_prefix:str, template_key: str, session: Session) -> Presenter:
        dialog_service = self._services.get(DialogService)
        render_service = self._services.get(RendererService)
        return Presenter(template_prefix, template_key, session, render_service, dialog_service)
    


async def ask(dialogs: DialogService, session: Session, prompt_text: str) -> str:
    """     
    Asks the user for free-text input based on a rendered template section.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        str: The user's input as a string.
    """
    await session.emit(prompt_text)

    return await dialogs.set_prompt(
        session, 
        timeout=settings.network.prompt_timed_out)


async def ask_secret(dialogs: DialogService, session: Session, prompt_text: str) -> str:
    
    await session.emit(prompt_text)
    
    return await dialogs.set_prompt(
        session,
        timeout=settings.network.prompt_timed_out,
        mode=PromptMode.SECRET
    )

async def confirm(dialogs: DialogService, session: Session, prompt_text: str) -> bool:
    """
    Asks the user for a yes/no confirmation using a template-based prompt.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        **data: Optional data passed to the template.

    Returns:
        bool: True if confirmed, False otherwise.
    """
    while True:
        answer = await ask(dialogs, session, prompt_text)
        if answer.lower() in ("y", "yes", "j", "ja"):
            return True
        if answer.lower() in ("n", "no", "nein"):
            return False
        await session.emit("Bitte antworte mit 'y' oder 'n'.")


async def choice(dialogs: DialogService, session: Session, prompt_text: str, options: list[str]) -> str:
    """
    Presents the user with a list of choices and returns the selected value.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        str: The chosen value.
    """
    options_str = ", ".join(options)
    while True:
        answer = await ask(dialogs, session, prompt_text)
        if answer in options:
            return answer
        await session.emit(f"Bitte wähle eine der Optionen: {options_str}")


async def choice_index(dialogs: DialogService, session: Session, prompt_text: str, options: list[str]) -> str:
    """
    Presents the user with a numbered list of choices and returns the selected index.

    Args:
        session: BaseSession: The session passed to the template.
        section (str): The section key within the template.
        choices (list[str]): List of available options.
        **data: Optional data passed to the template.

    Returns:
        int: The index of the selected choice (starting at 0).
    """
    if not options:
        raise ValueError("choice() requires at least one option.")

    # Ausgabe der nummerierten Liste
    msg = [prompt_text]
    for idx, opt in enumerate(options, 1):
        msg.append(f"[{idx}] {opt}")
    await session.emit("\n".join(msg))

    # Dialogschleife
    while True:
        answer = await ask(dialogs, session, prompt_text)
        if answer.isdigit():
            index = int(answer) - 1
            if 0 <= index < len(options):
                return index, options[index]
        await session.emit("Bitte eine gültige Nummer eingeben.")