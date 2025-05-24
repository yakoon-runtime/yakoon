
def split_batch_input(input_str: str, prefix: str = "batch:", max_parts: int = 10) -> list[str]:
    """
    Splits a batch command string into multiple commands.

    Args:
        input_str: Raw input string (should start with 'batch:')
        prefix: The prefix that triggers batch parsing.
        max_parts: Maximum number of commands to return.

    Returns:
        A list of cleaned command strings.
    """
    input_str = input_str.strip()
    if not input_str.startswith(prefix):
        return [input_str]
    parts = [s.strip() for s in input_str[len(prefix):].split(";") if s.strip()]
    return parts[:max_parts]
