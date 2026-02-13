from enum import StrEnum


class InteractionMode(StrEnum):
    """
    Defines the available interaction modes for handling user inputs.
    """

    WIZARD = "wizard"
    FORM = "form"

    @classmethod
    def values(cls) -> set[str]:
        return {v.value for v in cls}
