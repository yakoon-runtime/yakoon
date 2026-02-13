from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.prompt import PromptMode
from yakoon.base.ports import DialogService
from yakoon.base.runtime.session import Session

from yakoon.platform.settings import settings


class PromptService:
    """
    Thin adapter around DialogService that provides
    structured prompt helpers for workflows and commands.
    """

    def __init__(self, services: ServiceDirectory):
        self._services = services

    async def ask(self, session: Session, prompt_text: str) -> str:
        await session.emit(prompt_text)
        dialogs = self._services.get(DialogService)
        return await dialogs.set_prompt(
            session,
            timeout=settings.network.prompt_timed_out,
        )

    async def ask_secret(self, session: Session, prompt_text: str) -> str:
        await session.emit(prompt_text)
        dialogs = self._services.get(DialogService)
        return await dialogs.set_prompt(
            session,
            timeout=settings.network.prompt_timed_out,
            mode=PromptMode.SECRET,
        )

    async def confirm(self, session: Session, prompt_text: str) -> bool:
        while True:
            answer = await self.ask(session, prompt_text)
            a = str(answer or "").strip().casefold()

            if a in ("y", "yes", "j", "ja"):
                return True
            if a in ("n", "no", "nein"):
                return False

            await session.emit("Bitte antworte mit 'y' oder 'n'.")

    async def choice_value(
        self,
        session: Session,
        prompt_text: str,
        options: list[dict],
        *,
        default: str | None = None,
    ) -> str:

        if not options:
            raise ValueError("choice_value() requires at least one option")

        # ---- validate & normalize options (fail fast) ----
        norm: list[tuple[str, str]] = []
        values: set[str] = set()

        for opt in options:
            if "label" not in opt or "value" not in opt:
                raise ValueError("choice_value() options require keys: label, value")

            label = str(opt["label"])
            value = str(opt["value"])

            if value in values:
                raise ValueError(f"choice_value(): duplicate option value: {value!r}")

            values.add(value)
            norm.append((label, value))

        if default is not None:
            d = str(default)
            if d not in values:
                raise ValueError(f"choice_value(): default {d!r} not in option values")

        # ---- show options ----
        lines = [prompt_text]
        for idx, (label, _) in enumerate(norm, 1):
            lines.append(f"[{idx}] {label}")
        await session.emit("\n".join(lines))

        # ---- ask loop ----
        while True:
            answer = await self.ask(session, prompt_text)
            a = str(answer or "").strip()

            # empty input -> default
            if not a and default is not None:
                return str(default)

            # numeric selection
            if a.isdigit():
                i = int(a) - 1
                if 0 <= i < len(norm):
                    return norm[i][1]

            # label/value match
            ac = a.casefold()
            for label, value in norm:
                if ac == label.casefold() or ac == value.casefold():
                    return value

            await session.emit("Bitte eine gültige Auswahl treffen.")

    async def choice_index(
        self, session: Session, prompt_text: str, options: list[str]
    ) -> int:

        if not options:
            raise ValueError("choice_index() requires at least one option")

        lines = [prompt_text]
        for idx, opt in enumerate(options, 1):
            lines.append(f"[{idx}] {opt}")
        await session.emit("\n".join(lines))

        while True:
            answer = await self.ask(session, prompt_text)
            a = str(answer or "").strip()

            if a.isdigit():
                index = int(a) - 1
                if 0 <= index < len(options):
                    return index

            await session.emit("Bitte eine gültige Nummer eingeben.")
