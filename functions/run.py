from smolagents import tool
from llm import context
import subprocess
import sys
import os


@tool
def run_python() -> str:
    """
    Runs the last opened python file
    Returns:
        The exact output of the run
    """
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
        return result.stdout

    except Exception as e:
        return f"Error while running the application: {e}"