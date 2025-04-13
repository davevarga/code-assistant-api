import os
from dotenv import load_dotenv
from openai import OpenAI

from functions import tools, tool_functions
from llm.handler import EventHandler
from llm import context


# Import environment variables from .env file
load_dotenv('.env')
OPENAI_API_KEY = os.environ.get('API_KEY')
SERPER_API_KEY = os.environ.get('SERPER_APIKEY')

# Create the first llm
client = OpenAI(api_key=OPENAI_API_KEY)


if __name__ == '__main__':
    thread = client.beta.threads.create()
    assistant_id = "asst_YeklFmgl6c5i9AZG1V85Qiy4"

    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tools=tools,
        instructions="You are a personal math tutor. Write and run code to answer math questions."
    )
    message = (
        "Write a Python function simulate_game(commands:"
        " List[str]) -> Dict[str, Any] that simulates a simple strategy game."
        " Each command in the list represents an action taken by a player in"
        " the game. The game supports the following commands (case-sensitive strings):"

        "'GATHER <resource> <amount>': adds <amount> units of <resource>"
        " to the player's inventory. Supported resources: 'wood', 'stone', 'food'."

        "'BUILD <structure>': builds a structure using available resources."
        " Supported structures:"
        "'house' requires 20 wood and 5 food."
        "'barracks' requires 50 wood, 30 stone."
        "'farm' requires 10 wood, 10 food."

        "'STATUS': prints current resource inventory and built structures."
        "Your function should process each command and"
        "return a dictionary summarizing:"

        "'inventory': a dictionary of remaining resources."
        "structures: a list of built structures, in the order they were built."
        "errors: a list of error messages encountered (e.g., if a build command fails due to insufficient resources or unknown structure)."
        "Implement the function to correctly manage the resource state across commands and to gracefully handle unknown or malformed commands."
    )
    response = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )
    # Pass all available tools to the handler
    handler = EventHandler(client, tool_functions)

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=handler,
    ) as stream:
        stream.until_done()