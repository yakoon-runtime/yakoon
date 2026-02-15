import re

from yakoon.base.models.fields import FieldSpec, FieldType, SecretValue, SelectOption
from yakoon.base.models.policy import (
    FieldPolicy,
    PolicyValidationError,
    PolicyValidationResult,
    RawValue,
)


class PolicyService:
    def __init__(self):
        self._policies: dict[str, FieldPolicy] = {}
        self._validators: dict[str, callable] = {}

    def register_policy(self, policy: FieldPolicy) -> None:
        self._policies[policy.key] = policy

    def register_policies(self, policies: list[FieldPolicy]) -> None:
        for p in policies:
            self.register_policy(p)

    def get_policy(self, key: str) -> FieldPolicy:
        try:
            return self._policies[key]
        except KeyError as e:
            raise KeyError(f"Unknown policy '{key}'") from e

    def register_validator(self, key: str, fn) -> None:
        self._validators[key] = fn

    def get_validator(self, key: str) -> callable:
        return self._validators[key]

    def register_defaults(self):
        self.register_policies(
            [
                FieldPolicy(key="system:string", type=FieldType.STRING),
                FieldPolicy(key="system:masked", type=FieldType.STRING, secret=True),
                FieldPolicy(key="system:int", type=FieldType.INT),
                FieldPolicy(key="system:bool", type=FieldType.BOOL),
                FieldPolicy(
                    key="system:email",
                    type=FieldType.STRING,
                    hint="name@example.com",
                    pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                ),
            ]
        )

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

    def materialize_field(
        self,
        policy_key: str,
        *,
        key: str,
        label: str,
        required: bool | None = None,
        hint: str | None = None,
        secret: bool | None = None,
        options: list[dict] | None = None,
        default: object | None = None,
    ) -> FieldSpec:
        pol = self.get_policy(policy_key)

        # base from policy
        opt = options if options is not None else (pol.options or None)
        sel = (
            None
            if not opt
            else [SelectOption(value=o["value"], label=o["label"]) for o in opt]
        )

        return FieldSpec(
            key=key,
            label=label,
            type=pol.type,
            required=pol.required if required is None else required,
            hint=pol.hint if hint is None else hint,
            secret=pol.secret if secret is None else secret,
            pattern=pol.pattern,
            default=pol.default if default is None else default,
            options=sel,
            # if you add validators to FieldSpec:
            validators=pol.validators,
        )

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
            if v in {"true", "t", "1", "yes", "y", "ja", "j"}:
                return True
            if v in {"false", "f", "0", "no", "n", "nein"}:
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
