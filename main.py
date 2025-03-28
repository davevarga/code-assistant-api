import os
from dotenv import load_dotenv
from openai import OpenAI

from functions import show_tool, create_tool, open_tool, insert_tool
from llm.handler import EventHandler


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
        tools=[show_tool, create_tool, open_tool, insert_tool]
    )

    message = ("Create a python file called fibonacci.py Implement in this file"
               "a fibonacci sequence with a recursive funciton.")
    response = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler(client)
    ) as stream:
        stream.until_done()