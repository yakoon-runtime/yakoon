from dataclasses import dataclass, replace
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class SelectOption:
    value: str
    label: str


class FieldType(StrEnum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DATE = "date"
    SELECT = "select"


@dataclass(frozen=True)
class SecretValue:
    value: str

    def reveal(self) -> str:
        return self.value

    def __str__(self) -> str:
        return "******"

    def __repr__(self) -> str:
        return "SecretValue(******)"


@dataclass(frozen=True, slots=True)
class FieldSpec:
    key: str
    label: str | None = None
    type: FieldType = FieldType.STRING
    required: bool = False
    hint: str = ""
    secret: bool = False
    options: list[SelectOption] | None = None

    def fork(self, **changes) -> "FieldSpec":
        return replace(self, **changes)


@dataclass(frozen=True, slots=True)
class FormSpec:
    batch_id: str
    step_key: str
    form_id: str
    title: str | None = None
    fields: list[FieldSpec] = ()


@dataclass(frozen=True, slots=True)
class FormSubmission:
    batch_id: str
    form_id: str
    values: dict[str, object]  # values raw; conversion is server-side
