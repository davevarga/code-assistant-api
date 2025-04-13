import re

from llm import context
import subprocess
import sys
import os


edit_tool = {
    "type": "function",
    "function": {
        "name": "run",
        "description": "Edits an open file. An interval of code snippet is given,"
                       "and the content in the code captured by the code snippet"
                       "is changed to the given content. Use multiple edit commands"
                       "instead of congesting into a single one.",
        "parameters": {
            "type": "object",
            "properties": {
                "from": {
                    "type": "number",
                    "description": "Marks the beginning of the interval"
                                   "where the code snippet should be replaced"
                },
                "to": {
                    "type": "number",
                    "description": "Marks the end of the interval. All code"
                                   "between the beginning and end of the interval"
                                   "will be replaced"
                },
                "code": {
                    "type": "string",
                    "description": "The python code to be inserted between the lines"
                }
            },
            "required": ["from", "to"],
            "additionalProperties": False
        }
    }
}
def response_formatter(output, errors, status) -> str:
    header = [f"Running {context.get()} with exit code {status}:"]
    if status != 0:
        for line in errors.split("\n"):
            line = line.replace("")

    output = output or ["The application ran successfully but produced no output."]
    return "\n".join(header + output)

def run() -> str:
    file_path = context.get_abs()
    if not os.path.isfile(file_path):
        return f"Error: File '{file_path}' does not exist."

    if not file_path.endswith('.py'):
        return f"Error: '{file_path}' is not a Python file."

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        output = result.stdout
        errors = result.stderr
        status = result.returncode
        return response_formatter(output, errors, status)

    except Exception as e:
        return f"Error while running the application: {e}"