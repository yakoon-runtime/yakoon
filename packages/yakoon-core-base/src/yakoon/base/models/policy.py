from dataclasses import dataclass
from typing import TypeAlias

RawValue: TypeAlias = object
CoercedValue: TypeAlias = object


@dataclass(frozen=True, slots=True)
class PolicyValidationError:
    field_key: str
    message: str


@dataclass(frozen=True, slots=True)
class PolicyValidationResult:
    ok: bool
    value: object | None = None
    errors: list[PolicyValidationError] = ()
