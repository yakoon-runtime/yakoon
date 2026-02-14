from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.fields import FieldSpec, FieldType
from yakoon.base.runtime.session import Session
from yakoon.platform.settings import settings


class PromptService:
    """
    Thin adapter around DialogService that provides
    structured prompt helpers for workflows and commands.
    """

    def __init__(self, services: ServiceDirectory):
        self._services = services

    async def ask(self, session: Session, field: FieldSpec) -> object:
        dialogs = self._services.get(ports.DialogService)
        return await dialogs.wait_field(
            session,
            field=field,
            timeout=settings.network.prompt_timed_out,
        )

    async def confirm(self, session: Session, field: FieldSpec) -> bool:
        while True:
            answer = await self.ask(session, field)
            a = str(answer or "").strip().casefold()

            if a in ("y", "yes", "j", "ja"):
                return True
            if a in ("n", "no", "nein"):
                return False

            await session.emit("Bitte antworte mit 'y' oder 'n'.")

    async def choice_value(
        self,
        session: Session,
        field: FieldSpec,
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
        lines = [field.label]
        for idx, (label, _) in enumerate(norm, 1):
            lines.append(f"[{idx}] {label}")
        await session.emit("\n".join(lines))

        # ---- ask loop ----
        while True:
            answer = await self.ask(session, field)
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
        self, session: Session, field: FieldSpec, options: list[str]
    ) -> int:

        if not options:
            raise ValueError("choice_index() requires at least one option")

        lines = [field.label]
        for idx, opt in enumerate(options, 1):
            lines.append(f"[{idx}] {opt}")
        await session.emit("\n".join(lines))

        while True:
            answer = await self.ask(session, field)
            a = str(answer or "").strip()

            if a.isdigit():
                index = int(a) - 1
                if 0 <= index < len(options):
                    return index

            await session.emit("Bitte eine gültige Nummer eingeben.")

    def _coerce(self, field: FieldSpec, value: object) -> object:
        if value is None:
            return None

        raw = str(value).strip()

        if field.type == FieldType.STRING:
            return raw

        if field.type == FieldType.INT:
            try:
                return int(raw)
            except ValueError:
                raise ValueError(f"Invalid integer for '{field.key}'") from ValueError

        if field.type == FieldType.FLOAT:
            try:
                return float(raw)
            except ValueError:
                raise ValueError(f"Invalid float for '{field.key}'") from ValueError

        if field.type == FieldType.BOOL:
            lowered = raw.lower()
            if lowered in ("y", "yes", "true", "1"):
                return True
            if lowered in ("n", "no", "false", "0"):
                return False
            raise ValueError(f"Invalid boolean for '{field.key}'")

        if field.type == FieldType.SELECT:
            valid = {opt.value for opt in (field.options or [])}
            if raw in valid:
                return raw
            raise ValueError(f"Invalid selection for '{field.key}'")

        return raw
