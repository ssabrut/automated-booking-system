import os

from src.config.memory import InMemoryHistory

from typing import Dict, Any
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_core.messages import (
    AIMessage, 
    HumanMessage
)
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

class ChatLLM:
    """
    The ChatLLM class is designed to interact with a language model from Hugging Face's Inference API. It allows for generating responses based on a given prompt and a memory of previous interactions.

    Attributes:
        max_tokens (int): The maximum number of tokens to generate in a single call to the language model.
        client (InferenceClient): An instance of the InferenceClient from the huggingface_hub library, initialized with the specified model and API key.
    """

    memories: InMemoryHistory = InMemoryHistory()
    
    def __init__(self, max_tokens: int = 100) -> None:
        """
        Initialize the ChatLLM

        Args:
            max_tokens (int, optional): The maximum number of tokens to generate in a single call to the LLM. Defaults to 100.
        """
        
        self.max_tokens = max_tokens
        self.client = InferenceClient(
            "meta-llama/Meta-Llama-3-8B-Instruct",
            token=HUGGINGFACE_API_KEY
        )

    def __call__(self, prompt: str, **kwarg: Any) -> Dict:
        """
        Run the LLM on the given input

        Args:
            memory (InMemoryHistory): An instance of InMemoryHistory containing previous outputs from the LLM and user inputs.
            **kwarg (Any): Additional keyword arguments to pass to the language model.

        Returns:
            Dict: The output from the LLM.
        """
        self.memories.add_messages([HumanMessage(content=prompt)])
        messages = self.memory_parser(self.memories)

        # Get the response from the LLM
        response = self.client.chat_completion(
            messages=messages,
            max_tokens=self.max_tokens
        )

        # Extract and clean the output message
        outputs = response.choices[0].message.__dict__
        outputs.pop("tool_calls", None)
        self.append_memory(outputs)
        return outputs

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set an attribute of the ChatLLM class.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to set the attribute to.
        """
        
        if name == "max_tokens" and not isinstance(value, int):
            raise ValueError("max_tokens must be an integer")
        super().__setattr__(name, value)

    def memory_parser(self, memory: InMemoryHistory) -> list:
        """
        Parse the memory to convert it into a format suitable for the LLM.

        Args:
            memory (InMemoryHistory): An instance of InMemoryHistory containing previous outputs from the LLM and user inputs.

        Returns:
            list: A list of parsed messages suitable for the LLM.
        """

        _memory = []
        
        for message in memory.messages:
            if message.__dict__["type"] == "human":
                _memory.append({
                    "role": "user",
                    "content": message.__dict__["content"]
                })
            else:
                _memory.append({
                    "role": "assistant",
                    "content": message.__dict__["content"]
                })
        return _memory

    def append_memory(self, response: Dict) -> AIMessage:
        """
        Append the AI's response to the memory.

        Args:
            memory (InMemoryHistory): An instance of InMemoryHistory containing previous outputs from the LLM and user inputs.
            response (Dict): The response from the LLM to be appended to the memory.

        Returns:
            AIMessage: The AIMessage instance containing the response content.
        """
        ai_message = AIMessage(content=response["content"])
        self.memories.add_ai_message(ai_message)
        return ai_message