from smolagents import Tool
from legacy.utils import ContextManager, ContextPermissionError, ContextError


class OpenTool(Tool):
    name = "open_file_or_directory"
    description = """Lets you navigate in the working directory, or open files for editing.
        To go back use the command with the argument: ../ Returns if the procedure was successful.
        If the 'home' argument is used, it will return the root directory."""
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
            if name == "home":
                self.context.set(self.context.get_root())
                assert self.context.get(abs=True) == self.context.get_root()
                return f"You are in the root directory: {self.context.get(abs=True)}\n"
            absolute_path = self.context.get(abs=True) / name
            self.context.set(absolute_path)
            return f"Successfully opened {self.context.get()}\n"
        except ContextPermissionError:
            return f"{name} permission denied\n"
        except ContextError:
            return (
                f"File does not exist in {self.context.get()} context.\n"
                f"Use this command with argument 'home' to go back to the root\n"
            )
