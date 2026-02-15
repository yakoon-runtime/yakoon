from __future__ import annotations

from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.fields import FieldSpec, FormSpec
from yakoon.base.runtime.session.session import Session
from yakoon.platform.settings import settings


class InputService:
    """
    Unified interaction layer.

    Always communicates with DialogService via FormSpec.
    A single field is represented as FormSpec with one field.
    """

    def __init__(self, services: ServiceDirectory):
        self._dialogs = services.get(ports.DialogService)
        self._policy = services.get(ports.PolicyService)

    # -----------------------------------------------------
    # Core
    # -----------------------------------------------------

    async def ask_form(self, session: Session, spec: FormSpec) -> dict[str, object]:
        """
        Central input mechanism.
        Waits for FormSpec submission, validates via PolicyService,
        repeats on validation errors.
        """
        while True:
            raw = await self._dialogs.wait_input(
                session,
                spec=spec,
                timeout=settings.network.prompt_timed_out,
            )

            errors = []
            out: dict[str, object] = {}

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
                errors.append(
                    type(
                        "Err",
                        (),
                        {
                            "field_key": "form",
                            "message": f"Unknown fields: {sorted(unknown)}",
                        },
                    )()
                )

            if not errors:
                return out

            for e in errors:
                await session.emit(f"[{e.field_key}] {e.message}")

    async def ask_field(self, session: Session, field: FieldSpec) -> object:
        """
        Convenience wrapper for single-field interaction.
        """
        spec = FormSpec(
            form_id=f"field:{field.key}",
            batch_id=None,
            step_key=None,
            title="",
            fields=[field],
        )

        values = await self.ask_form(session, spec)
        return values[field.key]

    # -----------------------------------------------------
    # Optional Wizard helpers (legacy convenience)
    # -----------------------------------------------------

    async def confirm(self, session: Session, field: FieldSpec) -> bool:
        """
        Could be replaced entirely by system:bool policy later.
        """
        field = field.copy_with(policy="system:bool")  # if you support cloning
        return bool(await self.ask_field(session, field))

    async def choice_value(
        self,
        session: Session,
        field: FieldSpec,
        options: list[dict],
        *,
        default: str | None = None,
    ) -> str:
        """
        This could also move to PolicyService later.
        For now implemented as form with options metadata.
        """
        field = field.copy_with(options=options, default=default)
        return str(await self.ask_field(session, field))

    async def choice_index(
        self,
        session: Session,
        field: FieldSpec,
        options: list[str],
    ) -> int:
        mapped = [{"label": opt, "value": str(i)} for i, opt in enumerate(options)]
        val = await self.choice_value(session, field, mapped)
        return int(val)
