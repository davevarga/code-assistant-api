import os
from smolagents import Tool
from utils import check_syntax, ContextManager


class InsertTool(Tool):
    name = "insert_code"
    description = """Insert the given code at the specified line number,
        in the last opened file. Feedback about the success of the insertion."""
    inputs = {
        "start": {
            "type": "number",
            "description": "The line before which the code will be inserted",
        },
        "code": {
            "type": "string",
            "description": "The python code to be inserted",
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, start: int, code: str) -> str:
        file_path = self.context.get(abs=True)
        if os.path.isdir(file_path):
            return (f"You are cure in {self.context.get()} directory. "
                    f"Use the open_file_or_directory tool to open a file "
                    f"or the create_file_or_directory tool to create one.")

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
            total_lines = len(lines)

            # Validate line interval
            start = max(start, 1)
            start = min(start, total_lines + 1)

            # Insert the new code at the correct position
            code_lines = [(line if line.endswith('\n') else line + '\n') for line in code.splitlines()]
            for i, line in enumerate(code_lines):
                lines.insert(start + i, line)
            total_lines += len(code_lines)

            # Make alterations only with syntactically correct code
            # In case of errors give feedback to the llm.
            errors = check_syntax('\n'.join(lines))

            # Write the modified content back to the file
            with open(file_path, "w") as file:
                file.writelines(lines)

            # Create response for the LLM
            response = [f"{i + start}: {line.rstrip()}\n"
                        for i, line in enumerate(code_lines)]

            if errors:
                # In case of erroneous code provide feedback
                response += ["(Code returned to following errors)\n"]
                response += "\n".join(errors) + '\n'

            # In case of syntax error free code give feedback
            header = [f"[File: {self.context.get()} ({total_lines} lines in total)]\n"]
            return "".join(header + response)

        except FileNotFoundError:
            return f"Error: File '{file_path}' not found."
        except Exception as e:
            return f"Error: {str(e)}"