import csv
import datetime

# from src.config.agents import Agent
# from langchain_core.messages import HumanMessage

# # Config agent
# agent = Agent()

# # Add messages to memory
# messages = [HumanMessage(content="Hello, I'm Bob!")]
# response = agent.invoke(messages)
# print(response)

selected_date = "2020-01-01"
selected_start_time = datetime.datetime.strptime("10:00", "%H:%M").time()
selected_end_time = datetime.datetime.strptime("12:00", "%H:%M").time()

# if selected_start_time <= temp <= selected_end_time:
#     print("temp is within the range")
# else:
#     print("temp is outside the range")

# with open("data/booking.csv", "r") as f:
#     reader = csv.reader(f)
#     next(reader)  # Skip header row
#     for row in reader:
#         name = row[1]
#         date = row[2]
#         start_time = datetime.datetime.strptime(row[3], "%H:%M").time()
#         end_time = datetime.datetime.strptime(row[4], "%H:%M").time()
#         if date == selected_date \
#             and selected_start_time <= start_time <= selected_end_time \
#                 and selected_start_time <= end_time <= selected_end_time:
#             print(name, date, start_time, end_time)

from src.config.agents import Agent
from langchain_core.tools import tool
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description

agent = Agent()

@tool
def add(x: float, y: float) -> float:
    """
    This function takes two float numbers as input and returns their sum.

    Parameters:
        x (float): The first number.
        y (float): The second number.

    Returns:
        float: The sum of x and y.
    """
    return x + y

tools = [add]
rendered_tools = render_text_description(tools)
system_prompt = f"""\
You are an assistant that has access to the following set of tools. 
Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. 
Return your response as a JSON blob with 'name' and 'arguments' keys.

The `arguments` should be a dictionary, with keys corresponding 
to the argument names and the values corresponding to the requested values.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

chain = prompt | agent
message = chain.invoke({"input": "what's 3 plus 1132"})

chain = prompt | agent | JsonOutputParser()

from typing import Any, Dict, Optional, TypedDict

from langchain_core.runnables import RunnableConfig


class ToolCallRequest(TypedDict):
    """A typed dict that shows the inputs into the invoke_tool function."""

    name: str
    arguments: Dict[str, Any]


def invoke_tool(
    tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None
):
    """A function that we can use the perform a tool invocation.

    Args:
        tool_call_request: a dict that contains the keys name and arguments.
            The name must match the name of a tool that exists.
            The arguments are the arguments to that tool.
        config: This is configuration information that LangChain uses that contains
            things like callbacks, metadata, etc.See LCEL documentation about RunnableConfig.

    Returns:
        output from the requested tool
    """
    tool_name_to_tool = {tool.name: tool for tool in tools}
    name = tool_call_request["name"]
    requested_tool = tool_name_to_tool[name]
    return requested_tool.invoke(tool_call_request["arguments"], config=config)

chain = prompt | agent | JsonOutputParser() | invoke_tool
print(chain.invoke({"input": "what's thirteen plus 4.14137281"}))

