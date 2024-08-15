# import csv
# import datetime

# # from src.config.agents import Agent
# # from langchain_core.messages import HumanMessage

# # # Config agent
# # agent = Agent()

# # # Add messages to memory
# # messages = [HumanMessage(content="Hello, I'm Bob!")]
# # response = agent.invoke(messages)
# # print(response)

# # if selected_start_time <= temp <= selected_end_time:
# #     print("temp is within the range")
# # else:
# #     print("temp is outside the range")

# # with open("data/booking.csv", "r") as f:
# #     reader = csv.reader(f)
# #     next(reader)  # Skip header row
# #     for row in reader:
# #         name = row[1]
# #         date = row[2]
# #         start_time = datetime.datetime.strptime(row[3], "%H:%M").time()
# #         end_time = datetime.datetime.strptime(row[4], "%H:%M").time()
# #         if date == selected_date \
# #             and selected_start_time <= start_time <= selected_end_time \
# #                 and selected_start_time <= end_time <= selected_end_time:
# #             print(name, date, start_time, end_time)

# selected_date = "2020-01-01"
# selected_start_time = datetime.datetime.strptime("10:00", "%H:%M").time()
# selected_end_time = datetime.datetime.strptime("10:10", "%H:%M").time()

from src.config.agents import Agent
from src.tools.rag import check_name, check_date
from src.tools.properties import booking
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
from typing import Any, Dict, Optional, TypedDict
from langchain_core.runnables import RunnableConfig

agent = Agent()

tools = [check_name, check_date]
rendered_tools = render_text_description(tools)
system_prompt = f"""\
You are an assistant that has access to the following set of tools. 
Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. 
Return your response as a JSON blob with 'name' and 'arguments' keys.

If the input contains the word "name", refine the prompt to specifically check for the presence of a name in the booking system.
If the input contains the word "date", refine the prompt to specifically check for the presence of a date in the booking system. Convert the date string to "YYYY-MM-DD" format. The month can be in numerical format (e.g., "03" for March) or text format (e.g., "March" or "Mar" or "march" or "mar").
If the input contains the word "start_time", refine the prompt to specifically check for the presence of a start time in the booking system.
If the input contains the word "end_time", refine the prompt to specifically check for the presence of an end time in the booking system.

The `arguments` should be a dictionary, with keys corresponding 
to the argument names and the values corresponding to the requested values.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)


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
print(chain.invoke({"input": "I want to book in january 1, 2024"}))
print(booking.__dict__)