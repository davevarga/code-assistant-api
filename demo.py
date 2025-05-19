import os
from smolagents import ToolCallingAgent, LiteLLMModel, DuckDuckGoSearchTool, tool
from smolagents import ActionStep, TaskStep, SystemPromptStep

# Environment variables are loaded from a .env file
from dotenv import load_dotenv
from smolagents.memory import MemoryStep

load_dotenv('.env')


class WebSearchTool(DuckDuckGoSearchTool):
    """
    A simple web search tool that uses DuckDuckGo to search the web.
    """
    def __init__(self):
        super().__init__()

    def run(self, query: str) -> str:
        return super().run(query)

    def compress(self) -> str:
        """
        Compress the response to a more concise format.
        """
        return 'compress'



if __name__ == '__main__':
    llm_model = LiteLLMModel(
        model_id="openai/gpt-4.1-mini",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    agent = ToolCallingAgent(
        model=llm_model,
        tools=[WebSearchTool()]
    )
    agent.run("Who is the current president of Romania?", reset=False)

    for previouse_memory_step in agent.memory.steps:
        print(type(previouse_memory_step))

        if isinstance(previouse_memory_step, ActionStep):
            if previouse_memory_step.tool_calls[0].name == "web_search":

                compressed_tool_output = agent.tools['web_search'].compress()
                print(compressed_tool_output)
                print(previouse_memory_step.observations)

            if previouse_memory_step.tool_calls[0].name == "final_answer":
                print('FinalAnswerTool Recognized')
                tool_output = previouse_memory_step.action_output
                print(tool_output)
                print(previouse_memory_step.observations)

                for message in previouse_memory_step.model_input_messages:
                    print(message['role'], message['content'])


