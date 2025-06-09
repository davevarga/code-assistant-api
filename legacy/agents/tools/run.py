from smolagents import Tool
import subprocess
import sys
import os

from legacy.utils import ContextManager


class RunTool(Tool):
    name = "run_python"
    description = """Runs the last opened python file. 
        Use this tool to validate your code,
        and to check for syntax and runtime errors."""
    inputs = {}
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self) -> str:
        file_path = self.context.get(abs=True)
        if os.path.isdir(file_path):
            return (f"You are cure in {self.context.get()} directory."
                    f"Use the open_file_or_directory tool to open a file.")
        if file_path.suffix != '.py':
            return (f"Error: '{file_path}' is not a Python file."
                    f"Use the open_file_or_directory tool to open a python file.")
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )
            return (
                f"Stdout:\n{result.stdout}\n"
                f"Stderr:\n{result.stderr}"
            )
        except Exception as e:
            return f"Error while running the application: {e}"