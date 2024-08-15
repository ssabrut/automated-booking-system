import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=HUGGINGFACE_API_KEY,
)

for message in client.chat_completion(
	messages=[{"role": "user", "content": "What is the capital of France?"}],
	max_tokens=500,
	stream=True,
):
    print(message.choices[0].delta.content, end="")
