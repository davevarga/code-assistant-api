from smolagents import Tool
from utils import ContextManager, ContextPermissionError, ContextError


class OpenTool(Tool):
    name = "open_file_or_directory"
    description = """Lets you navigate in the working directory, or open files for editing.
        To go back use the command with the argument: ../ Returns if the procedure was successful."""
    inputs = {
        "name": {
            "type": "string",
            "description": "Relative path of the file or directory."
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, name: str) -> str:
        try:
            absolute_path = self.context.get() / name
            self.context.set(absolute_path)
            return f"Successfully opened {self.context.get()}"
        except ContextPermissionError:
            return f"{name} permission denied"
        except ContextError:
            return f"File does not exist in {self.context.get()}"
