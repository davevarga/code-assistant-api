import re

from llm import context
import subprocess
import sys
import os


run_tool = {
    "type": "function",
    "function": {
        "name": "run",
        "description": "Runs the last opened python file. "
                       "Returns the exact output of the run"
                       "In case of errors, a detailed description will be provided.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
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