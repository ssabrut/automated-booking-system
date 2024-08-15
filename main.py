from src.config.agents import Agent
from langchain_core.messages import HumanMessage

# Config agent
agent = Agent()

# Add messages to memory
messages = [HumanMessage(content="Hello, I'm Bob!")]
response = agent.invoke(messages)
print(response)