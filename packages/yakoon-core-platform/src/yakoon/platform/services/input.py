from __future__ import annotations

from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.fields import FieldSpec, FormSpec
from yakoon.base.runtime.session.session import Session
from yakoon.platform.settings import settings


class InputService:
    """
    Interaction patterns built on top of:
      - DialogService (dialog)
      - PolicyService (validation/coercion/secret wrapping)

    This is reusable by Presenter and Workflows.
    """

    def __init__(self, services: ServiceDirectory):
        self._dialogs = services.get(ports.DialogService)
        self._policy = services.get(ports.PolicyService)

    async def ask(self, session: Session, field: FieldSpec) -> object:
        return await self._dialogs.wait_field(
            session,
            field=field,
            timeout=settings.network.prompt_timed_out,
        )

    async def ask_field(self, session: Session, field: FieldSpec) -> object:
        while True:
            raw = await self.ask(session, field)
            res = self._policy.validate_field(field=field, raw=raw)
            if res.ok:
                return res.value
            for err in res.errors:
                await session.emit(f"[{err.field_key}] {err.message}")

    async def ask_form(self, session: Session, spec: FormSpec) -> dict[str, object]:
        while True:
            raw = await self._dialogs.wait_form(session, spec=spec, timeout=...)
            errors = []
            out = {}

            for field in spec.fields:
                val = raw.get(field.key)
                res = self._policy.validate_field(field=field, raw=val)
                if res.ok:
                    out[field.key] = res.value
                else:
                    errors.extend(res.errors)

            # unknown keys?
            unknown = set(raw.keys()) - {f.key for f in spec.fields}
            if unknown:
                errors.append(ValueError("form", f"Unknown fields: {sorted(unknown)}"))

            if not errors:
                return out

            for e in errors:
                await session.emit(f"[{e.field_key}] {e.message}")

    async def confirm(self, session: Session, field: FieldSpec) -> bool:
        """
        Classic wizard confirm: y/n loop.
        (Alternatively you can model this as system:bool in PolicyService later.)
        """
        while True:
            raw = await self.ask(session, field)
            a = str(raw or "").strip().casefold()

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
        """
        Classic wizard choice:
          - prints options
          - accepts number or label/value
          - returns option value
        """
        if not options:
            raise ValueError("choice_value() requires at least one option")

        # validate & normalize options
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

        if default is not None and str(default) not in values:
            raise ValueError(
                f"choice_value(): default {default!r} not in option values"
            )

        # show options (wizard UX)
        lines = [field.label]
        for idx, (label, _) in enumerate(norm, 1):
            lines.append(f"[{idx}] {label}")
        await session.emit("\n".join(lines))

        # ask loop
        while True:
            raw = await self.ask(session, field)
            a = str(raw or "").strip()

            if not a and default is not None:
                return str(default)

            if a.isdigit():
                i = int(a) - 1
                if 0 <= i < len(norm):
                    return norm[i][1]

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
            raw = await self.ask(session, field)
            a = str(raw or "").strip()

            if a.isdigit():
                index = int(a) - 1
                if 0 <= index < len(options):
                    return index

            await session.emit("Bitte eine gültige Nummer eingeben.")
