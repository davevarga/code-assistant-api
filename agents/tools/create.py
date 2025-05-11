from smolagents import Tool
from utils import ContextManager


class CreateTool(Tool):
    name = "create_file_or_directory"
    description = """It creates either a file or directory in the current directory.
        A file is created if an extension is provided. Otherwise, it
        creates a new directory."""
    inputs = {
        "name": {
            "type": "string",
            "description": "Name of the file or directory.",
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, name: str) -> str:
        curr_dir = self.context.get(abs=True)
        path = curr_dir / name

        # Check if is already created
        if path.exists(): return "File or directory already exists"
        path = path.resolve(strict=False)
        try:
            if path.suffix:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            else:
                path.mkdir(parents=True)
        except FileExistsError:
            return "File already exists in the current location "
        except Exception as e:
            return f"Error while creating: {e}"

        # Return with the path of the created file.
        return f"{path.name} created successfully"