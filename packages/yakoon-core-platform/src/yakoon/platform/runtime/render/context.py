class RenderContext:
    """
    Defines the technical rendering context for a command output.

    Specifies which template path and language variant should be used.
    This separates language selection and routing logic from actual content data.

    Attributes:
        key (str): Template identifier (e.g. 'account/cmd_login').
        lang (str): Language code (e.g. 'de', 'en').
    """

    def __init__(self, key: str, prefix: str, lang: str):
        self.key = key
        self.lang = lang
        self.prefix = prefix
        self.format = format
