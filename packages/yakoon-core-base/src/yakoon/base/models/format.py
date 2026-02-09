from enum import Enum


class OutputFormat(str, Enum): 
    """
    Defines the available output formats for template rendering.
    """
    ANSI = "ansi"
    MARKDOWN = "md"
    PLAIN = "plain"

    @classmethod
    def values(cls) -> set[str]:
        return {v.value for v in cls}