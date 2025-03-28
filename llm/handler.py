import json
import os

from openai import AssistantEventHandler
from typing_extensions import override

from functions.create import create, open_file
from functions.show import extract_code_snippet
from functions.edit import insert_code_at_line


class EventHandler(AssistantEventHandler):

    def __init__(self, client, file=None):
        super(EventHandler, self).__init__()
        self.opened_file = file
        self.client = client

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
            if tool.function.name == "create":
                arguments = json.loads(tool.function.arguments)
                status = create(**arguments)
                print(status)
                tool_outputs.append({"tool_call_id": tool.id, "output": status})

            elif tool.function.name == "open":
                # This file is currently opened in the llm context
                arguments = json.loads(tool.function.arguments)
                self.opened_file = arguments.get("file_name")
                response = open_file(self.opened_file)
                print(response)
                tool_outputs.append({"tool_call_id": tool.id, "output": response})

            elif tool.function.name == "show":
                if self.opened_file is None:
                    output = "No file opened yet. Use the open function to open a file"
                    print(output)
                    tool_outputs.append({"tool_call_id": tool.id, "output": output})
                else:
                    arguments = json.loads(tool.function.arguments)
                    smart_content = extract_code_snippet(self.opened_file, **arguments)
                    print(smart_content)
                    tool_outputs.append({"tool_call_id": tool.id, "output": smart_content})

            elif tool.function.name == "insert":
                if self.opened_file is None:
                    output = "No file opened yet. Use the open function to open a file"
                    print(output)
                    tool_outputs.append({"tool_call_id": tool.id, "output": output})
                else:
                    arguments = json.loads(tool.function.arguments)
                    smart_content = insert_code_at_line(self.opened_file, **arguments)
                    print(smart_content)
                    tool_outputs.append({"tool_call_id": tool.id, "output": smart_content})

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.client, self.opened_file),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()