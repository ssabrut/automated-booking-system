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
from src.tools.rag import check_name, check_date, check_start_time, check_end_time, check_time_range
from src.tools.properties import booking
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
from typing import Any, Dict, Optional, TypedDict
from langchain_core.runnables import RunnableConfig

agent = Agent()

tools = [check_name, check_date, check_start_time, check_end_time, check_time_range]
tools_map = {tool.name: tool for tool in tools}
rendered_tools = render_text_description(tools)
system_prompt = f"""\
You are an assistant that has access to the following set of tools. 
Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the names and inputs of the tools to use. 
Return your response as a JSON blob with a 'tools' key. The value of 'tools' should be a list of dictionaries, each containing 'name' and 'arguments' keys.

If the input contains the word "name", refine the prompt to specifically check for the presence of a name in the booking system.
If the input contains the word "date", refine the prompt to specifically check for the presence of a date in the booking system. The date can be in "YYYY-MM-DD" format or "DD-MM-YYYY" format. Convert the date string to "YYYY-MM-DD" format. The month can be in numerical format (e.g., "03" for March) or text format (e.g., "March" or "Mar" or "march" or "mar").
If the input contains the word "start_time", refine the prompt to specifically check for the presence of a start time in the booking system. The time can be in numerical format (e.g., "14:00" for 2 PM) or text format (e.g., "2 PM" or "2 P.M."). Convert the time to 24-hour format if it is not already in that format. The time input could also be in a range format (e.g., "10 to 11" or "10-11"). Ensure both times in the range are converted to 24-hour format if they are not already.
If the input contains the word "end_time", refine the prompt to specifically check for the presence of an end time in the booking system. The time can be in numerical format (e.g., "18:00" for 6 PM) or text format (e.g., "6 PM" or "6 P.M."). Convert the time to 24-hour format if it is not already in that format. The time input could also be in a range format (e.g., "10 to 11" or "10-11"). Ensure both times in the range are converted to 24-hour format if they are not already.

If the input contains more than one property (e.g., name, date, start_time, end_time), call the corresponding tools in parallel.

After the user inputs "date", "start_time", and "end_time", check if the slot is available for booking.

The `tools` list should contain dictionaries, each with 'name' and 'arguments' keys, corresponding to the tools to be used and their respective arguments. The `arguments` should be a dictionary, with keys corresponding to the argument names and the values corresponding to the requested values.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)


class ToolCallRequest(TypedDict):
    """A typed dict that shows the inputs into the invoke_tool function."""

    name: str
    arguments: Dict[str, Any]


def invoke_tool(tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None):
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
    for tool in tool_call_request["tools"]:
        name = tool["name"]
        arguments = tool["arguments"]
        requested_tool = tools_map[name]
        requested_tool.invoke(arguments, config=config)
 
chain = prompt | agent | JsonOutputParser() | invoke_tool
# print(chain.invoke({"input": "My name is John Doe, and I would like to book an appointment for 10 to 11 on 2020-01-01"}))
# print(booking.__dict__)