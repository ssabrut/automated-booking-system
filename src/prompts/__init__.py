def system_prompt(rendered_tools: str) -> str:
    """
    Generate the system prompt by reading the template and formatting it with the rendered tools.

    Args:
        rendered_tools (str): A string containing the rendered tools to be included in the system prompt.

    Returns:
        str: The formatted system prompt.
    """
    with open("src/prompts/system", "r") as f:
        content = f.read()
    return content.format(rendered_tools=rendered_tools)