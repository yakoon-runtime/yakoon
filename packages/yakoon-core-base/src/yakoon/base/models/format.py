from enum import StrEnum


class OutputFormat(StrEnum):
    """
    Defines the available output formats for template rendering.
    """

    ANSI = "ansi"
    MARKDOWN = "md"
    PLAIN = "plain"

    @classmethod
    def values(cls) -> set[str]:
        return {v.value for v in cls}
