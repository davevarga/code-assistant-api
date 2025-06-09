import os
import time

from utils import CSVLogger, RepoHandler, ContextManager
from .tools import init_toolset
from smolagents import ToolCallingAgent, LiteLLMModel, Tool, ActionStep
from openinference.instrumentation import using_metadata

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

    def reset(self):
        self.agent.memory.reset()


class CodingAgent(LiteLLMAgent):
    def __init__(self,context_handler: ContextManager,  logger=None, **kwargs):
        super().__init__(logger)
        self.context_handler = context_handler
        self.tools = init_toolset(context_handler)
        self.agent = ToolCallingAgent(
            model=self.model, # Initiate agent with LiteLLM
            tools=self.tools,
            description=agent_description,
        )

    def insert_tool(self, tool: Tool):
        self.tools.append(tool)
        self.agent = ToolCallingAgent(
            model=self.model,
            tools=self.tools,
            description=agent_description,
        )

    def run(
        self,
        repo: RepoHandler,
        prompt: str,
        metadata = None
    ):
        # Make sure the repo is cloned
        assert repo.repo_path() is not None, \
            f"Agent run before cloning the repo"
        self.context_handler.set(repo.repo_path())

        # Metadata for Phoenix telemetry details
        # Solve problem with Agent
        t_start = time.time()
        with using_metadata(metadata if metadata is not None else {}):
            final_answer = self.agent.run(prompt, reset=False)
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

    def reset(self):
        self.agent.memory.reset()
        self.agent.monitor.reset()