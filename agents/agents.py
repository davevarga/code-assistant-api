import os
import time
from smolagents import ToolCallingAgent, LiteLLMModel

from utils import CSVLogger, RepoHandler
from .tools import toolset


agent_description = (
    "You're a handy agent that can access projects, inspect and analyze the code,"
    "and make changes in the project in order to fix an issue "
    "The python interpreter tool can't access the variables and packages in the project, "
    "but you have at your disposal any necessary tool to search, navigate, change and execute"
    "python or any necessary files. "
    "Your job involves more action than thinking.."
)

class LiteLLMAgent:
    def __init__(self, logger: CSVLogger = None):
        # Here the environment should contain the OPENAI_API_KEY variable
        assert os.environ.get('OPENAI_API_KEY') is not None, "OPENAI_API_KEY is not set"
        self.model = LiteLLMModel(
            model_id="openai/gpt-4o-mini",
            api_key=os.environ.get('OPENAI_API_KEY')
        )
        self.agent = None
        self.logger = logger

    def run(self, repo: RepoHandler, prompt: str):
        # Solve problem with Agent
        t_start = time.time()
        final_answer = self.agent.run(prompt)
        diff = repo.diff()
        t_end = time.time()

        # Log agent run
        if self.logger:
            inference_time = t_end - t_start
            self.logger.log('total_steps', len(self.agent.memory.get_full_steps()))
            self.logger.log("inference_time", inference_time)

            # Calculate tokens using a specific model
            self.logger.log('output_tokens', self.agent.monitor.total_output_token_count)
            self.logger.log('input_tokens', self.agent.monitor.total_input_token_count)

        return diff, final_answer


class CodingAgent(LiteLLMAgent):
    def __init__(self, logger=None, **kwargs):
        super().__init__(logger)
        self.agent = ToolCallingAgent(
            model=self.model, # Initiate agent with LiteLLM
            tools=toolset,
            description=agent_description,
        )