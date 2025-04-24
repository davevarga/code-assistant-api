import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel

from functions import tools
from llm.handler import EventHandler
from llm import context


# Import environment variables from .env file
load_dotenv('.env')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


if __name__ == '__main__':
    # Chose LLM model for chat completions
    model = LiteLLMModel(
        model_id="openai/gpt-4o-mini",
        api_key=OPENAI_API_KEY
    )

    # Create code agent
    agent = CodeAgent(
        tools=tools,
        model=model,
        add_base_tools=True
    )

    agent.run("Write a functions in the fibonacci.py file,"
              "that returns the n-th fibonaci number."
              "Use the dynamic programming, to solve the problem in polynomial time.")
