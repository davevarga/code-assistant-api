import os
from dotenv import load_dotenv
from openai import OpenAI

from functions import tools, function_tools
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
        name="Software Engineer",
        assistant_id=assistant_id,
        tools=function_tools,
        instructions="Similarly to software engineers, your task is to solve coding problems"
                     ""
                     "You have a diverse toolset at your disposal, to manipulate the project, such as edit, "
                     "insert, run, etc require a file or directory to be opened. You can do this with the open tool,"
                     "which let's you navigate in the project. The last opened file or directory is the context, "
                     "in which many of the tools will be called."
                     ""
                     "First search through the project files, looking for the relevant parts for the task. After a picture"
                     "has been formulated about the code, iteratively make alterations to the project, and test, if the"
                     "current changes conform to the expectations.s"
                     ""
                     "Try to break up the solution code into logically structured parts, adhering to engineering"
                     "principles and providing an elegant solution to the task at hand."
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
    handler = EventHandler(client, tools)

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=handler,
    ) as stream:
        stream.until_done()

    # Retrieve all the conversation.
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"{message.role.upper()}: {message.content[0].text.value}\n")

    # Cumulate all the tokens
    prompt_tokens = completion_tokens = total_tokens = 0
    runs = client.beta.threads.runs.list(thread_id=thread.id)
    for run in runs:
        if run.usage:
            completion_tokens += run.usage.completion_tokens
            prompt_tokens += run.usage.prompt_tokens
            total_tokens += run.usage.total_tokens

    print(
        f"Prompt: {prompt_tokens}, "
        f"Completion: {completion_tokens}, "
        f"Total: {total_tokens}"
    )

