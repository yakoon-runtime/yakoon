from enum import Enum


class RenderMode(str, Enum): 
    """
    Defines the available output formats for template rendering.
    """
    ANSI = "ansi"
    MARKDOWN = "md"
    PLAIN = "plain"
