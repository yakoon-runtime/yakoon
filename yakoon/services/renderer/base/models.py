from enum import Enum


class RenderMode(str, Enum): 
    """
    Defines the available output formats for template rendering.
    """
    ANSI = "ansi"
    MARKDOWN = "md"
    PLAIN = "plain"


class RenderSection:
    """
    Identifies a specific output block within a command template.

    The `key` selects the relevant section in the template (e.g. "success", "error"),
    while `data` provides optional values to be injected into that block.

    This allows command templates to render different outcomes
    (e.g. success/failure/info) from a shared file, depending on context.

    Attributes:
        key (str): Name of the section to render inside the template.
        data (dict): Optional context values available to the template.
    """

    def __init__(self, key, data=None):
        self.key = key
        self.data = data or {}


class RenderContext:
    """
    Defines the technical rendering context for a command output.

    Specifies which template path and language variant should be used.
    This separates language selection and routing logic from actual content data.

    Attributes:
        key (str): Template identifier (e.g. 'account/cmd_login').
        lang (str): Language code (e.g. 'de', 'en').
    """
   
    def __init__(self, key, lang):
        self.key = key
        self.lang = lang

