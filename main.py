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
from src.prompts import system_prompt
from src.tools.properties import booking
from src.tools import rendered_tools, invoke_tool

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

agent = Agent()
prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt(rendered_tools)), ("user", "{input}")]
)

chain = prompt | agent | JsonOutputParser() | invoke_tool
print(chain.invoke({"input": "My name is Liefran, I want to book a meeting room on march 24, 2024 from 1AM to 5AM"}))
print(booking.__dict__)