import json
import os

from openai import AssistantEventHandler
from typing_extensions import override


class EventHandler(AssistantEventHandler):

    def __init__(self, client, tools):
        super(EventHandler, self).__init__()
        self.client = client
        # Dictionary with available function that can be called.
        self.tools = tools

    @override
    def on_event(self, event):
        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name in self.tools:
                print("Using: ", tool.function.name)
                arguments = json.loads(tool.function.arguments)
                response = self.tools[tool.function.name](**arguments)
                print(response)
                tool_outputs.append({"tool_call_id": tool.id, "output": response})

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.client, self.tools),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()

    def add_tool(self, function_name: str, function):
        self.tools[function_name] = function