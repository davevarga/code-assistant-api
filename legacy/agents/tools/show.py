from smolagents import Tool
from utils import ContextManager


#  Extracts a portion of a Python file, numbers each line,
#  and includes information about how many lines exist before and after the snippet


class ShowTool(Tool):
    name = "show_code"
    description = """Extracts and formats a snippet of code from the last opened file,
        numbering each line. Returns the code of the last opened file from
        the start to end."""
    inputs = {
        "start": {
            "type": "number",
            "description": "The first line to show"
        },
        "end": {
            "type": "number",
            "description": "The last line to show"
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, start: int, end: int) -> str:
        file_path = self.context.get(abs=True)
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
            total_lines = len(lines)

            # Validate line interval
            start = max(start, 1)
            start = min(start, total_lines - 1)
            end = min(end, total_lines - 1)
            end = max(end, 1)

            # Format resonse
            total = len(lines)
            before = start - 1
            after = total - end

            header = (f"[File: {self.context.get()} ({total} lines in total)]\n"
                      f"({before} lines before)") if before > 0 else "(start)"
            snippet = [f"{i + start}: {line.rstrip()}"
                       for i, line in enumerate(lines[start - 1:end])]
            footer = f"({after} lines after)" if after > 0 else "(end)"
            return "\n".join([header] + snippet + [footer]).strip()

        except FileNotFoundError:
            return (f"Error: File '{file_path}' not found in current directory."
                    f"Use the list function to list all the content")
        except Exception as e:
            return f"Error: {e}"