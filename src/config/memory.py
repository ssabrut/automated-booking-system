from typing import List
from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_core.messages import BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """
    The InMemoryHistory class is a concrete implementation of the BaseChatMessageHistory class.
    It stores chat messages in memory using a list.

    Attributes:
        messages (List[BaseMessage]): A list of chat messages stored in memory.
    """
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """
        Add a list of messages to the in-memory message history.

        Args:
            messages (List[BaseMessage]): A list of messages to add to the in-memory message history.
        """
        self.messages.extend(messages)

    def clear(self) -> None:
        """
        Clear all messages from the in-memory message history.
        """
        self.messages = []