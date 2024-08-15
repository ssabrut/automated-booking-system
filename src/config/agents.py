from src.config.llm import ChatLLM

from typing import Any, Dict
from langchain_core.language_models.llms import LLM

llm = ChatLLM()

class Agent(LLM):
    """
    The Nia class is a custom language model that extends the LLM class. It uses the ChatLLM instance to generate responses based on a given prompt and memory of previous interactions.
    """

    def _call(self, prompt: str, **kwarg: Any) -> Dict:
        """
        Generate a response from the language model based on the given prompt and memory.

        Args:
            prompt (str): The input prompt to run the language model on.
            memory (list): A list of previous outputs from the language model and user inputs. Defaults to None.
            **kwarg (Any): Additional keyword arguments to pass to the language model.

        Returns:
            Dict: The output from the language model.
        """
        
        outputs = llm(prompt, **kwarg)
        return outputs["content"]

    @property
    def _llm_type(self) -> str:
        """
        Get the type of language model used by this chat model. Used for logging purposes only.

        Args:
            None

        Returns:
            str: The type of language model used by this chat model.
        """
        
        return "ChatLLM"

def set_max_tokens(max_tokens: int) -> None:
    """
    Set the maximum number of tokens to generate in a single call to the language model.

    Args:
        max_tokens (int): The maximum number of tokens to generate in a single call to the language model.
    """
    
    llm.__setattr__("max_tokens", max_tokens)