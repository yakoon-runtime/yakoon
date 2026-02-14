import re

from yakoon.base.models.fields import FieldSpec, FieldType, SecretValue
from yakoon.base.models.policy import (
    PolicyValidationError,
    PolicyValidationResult,
    RawValue,
)


class PolicyService:
    """
    Central policy registry and validator/coercer for fields.

    - Stores FieldSpecs (type, required, secret, options, pattern, etc.)
    - Validates and coerces raw inputs into canonical values
    - Wraps secrets in SecretValue
    """

    def __init__(self):
        self._fields: dict[str, FieldSpec] = {}

    def register_field(self, spec: FieldSpec) -> None:
        self._fields[spec.key] = spec

    def register_fields(self, specs: list[FieldSpec]) -> None:
        for spec in specs:
            self._fields[spec.key] = spec

    def register_defaults(self):
        self.register_fields(
            [
                FieldSpec(key="system:string", type=FieldType.STRING),
                FieldSpec(key="system:secret", type=FieldType.STRING, secret=True),
                FieldSpec(key="system:int", type=FieldType.INT),
                FieldSpec(key="system:bool", type=FieldType.BOOL),
            ]
        )

    def get_field(self, key: str) -> FieldSpec:
        try:
            return self._fields[key]
        except KeyError:
            raise RuntimeError(f"Unknown field policy: {key}") from KeyError

    def validate_field(
        self, *, field: FieldSpec, raw: RawValue
    ) -> PolicyValidationResult:
        # normalize raw -> string when needed
        raw_str = "" if raw is None else str(raw).strip()

        # required
        if field.required and raw_str == "":
            return PolicyValidationResult(
                ok=False,
                errors=(PolicyValidationError(field.key, "Wert ist erforderlich."),),
            )

        # empty but not required: treat as None (or "" for STRING if you prefer)
        if raw_str == "":
            coerced: object = None
            return PolicyValidationResult(
                ok=True, value=self._wrap_secret(field, coerced)
            )

        # type coercion
        try:
            coerced = self._coerce(field, raw_str)
        except ValueError as e:
            return PolicyValidationResult(
                ok=False,
                errors=(PolicyValidationError(field.key, str(e)),),
            )

        # pattern (optional)
        pattern = getattr(field, "pattern", None)
        if pattern:
            if not re.fullmatch(pattern, str(coerced)):
                return PolicyValidationResult(
                    ok=False,
                    errors=(PolicyValidationError(field.key, "Ungültiges Format."),),
                )

        # select membership
        if field.type == FieldType.SELECT:
            opts = field.options or []
            valid = {o.value for o in opts}
            if str(coerced) not in valid:
                return PolicyValidationResult(
                    ok=False,
                    errors=(PolicyValidationError(field.key, "Ungültige Auswahl."),),
                )

        return PolicyValidationResult(ok=True, value=self._wrap_secret(field, coerced))

    def _coerce(self, field: FieldSpec, raw: str) -> object:
        t = field.type

        if t == FieldType.STRING:
            return raw

        if t == FieldType.INT:
            try:
                return int(raw)
            except ValueError:
                raise ValueError("Bitte eine ganze Zahl eingeben.") from ValueError

        if t == FieldType.FLOAT:
            try:
                return float(raw)
            except ValueError:
                raise ValueError("Bitte eine Zahl eingeben.") from ValueError

        if t == FieldType.BOOL:
            v = raw.lower()
            if v in ("y", "yes", "ja", "true", "1"):
                return True
            if v in ("n", "no", "nein", "false", "0"):
                return False
            raise ValueError("Bitte ja/nein eingeben.")

        if t == FieldType.DATE:
            # minimal: ISO only (YYYY-MM-DD). Later: locale parsing.
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
                return raw
            raise ValueError("Bitte Datum im Format YYYY-MM-DD eingeben.")

        if t == FieldType.SELECT:
            # Keep as string key, membership checked later above
            return raw

        return raw

    def _wrap_secret(self, field: FieldSpec, value: object) -> object:
        if getattr(field, "secret", False):
            # store secrets as SecretValue; None stays None
            if value is None:
                return SecretValue("")
            return SecretValue(str(value))
        return value
