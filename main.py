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