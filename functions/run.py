from smolagents import tool
from llm import context
import subprocess
import sys
import os


@tool
def run_python() -> str:
    """
    Runs the last opened python file. Use this tool to validate your code,
    and to check for syntax and runtime errors.
    Returns:
        (str): The exact output of the run
    """


    file_path = context.get_abs()
    if os.path.isdir(file_path):
        return (f"You are cure in {context.get()} directory."
                f"Use the open_file_or_directory tool to open a file.")

    if not file_path.endswith('.py'):
        return (f"Error: '{file_path}' is not a Python file."
                f"Use the open_file_or_directory tool to open a python file.")

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        return result.stdout

    except Exception as e:
        return f"Error while running the application: {e}"