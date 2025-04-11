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
        tools=tools
    )
    message = (
        "Create a python file called fibonacci.py Implement in this file"
        "a fibonacci sequence with a recursive function."
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