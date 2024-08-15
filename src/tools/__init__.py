from src.tools.rag import check_name, check_date, check_time_range
from typing import Any, Dict, Optional, TypedDict
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import render_text_description

tools = [check_name, check_date, check_time_range]
tools_map = {tool.name: tool for tool in tools}
rendered_tools = render_text_description(tools)

class ToolCallRequest(TypedDict):
    """A typed dict that shows the inputs into the invoke_tool function."""

    name: str
    arguments: Dict[str, Any]


def invoke_tool(tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None):
    """
    A function that we can use to perform a tool invocation.

    Args:
        tool_call_request (ToolCallRequest): A dict that contains the keys 'name' and 'arguments'.
            The 'name' must match the name of a tool that exists.
            The 'arguments' are the arguments to that tool.
        config (Optional[RunnableConfig]): Configuration information that LangChain uses that contains
            things like callbacks, metadata, etc. See LCEL documentation about RunnableConfig.

    Returns:
        Any: Output from the requested tool.
    """
    print(tool_call_request)
    for tool in tool_call_request["tools"]:
        name = tool["name"]
        arguments = tool["arguments"]
        requested_tool = tools_map[name]
        requested_tool.invoke(arguments, config=config)