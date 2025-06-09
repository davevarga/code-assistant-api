from smolagents import Tool
from legacy.utils import check_syntax, ContextManager


class EditTool(Tool):
    name = "edit_file"
    description = """Changes the code lines in the given interval, to the given code,
        in the code file that was last opened."""
    inputs = {
        "start": {
            "type": "number",
            "description": "The beginning of the snippet. The first line number is 1.",
        },
        "end": {
            "type": "number",
            "description": "The number of the last line to be replaced.",
        },
        "code": {
            "type": "string",
            "description": "Python code to be inserted. Line indentation is important.",
        }
    }
    output_type = "string"

    def __init__(self, context: ContextManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def forward(self, start: int, end: int, code: str) -> str :
        file_path = self.context.get(abs=True)
        if file_path.is_dir():
            return (f"You are currently in {self.context.get()} directory. "
                    f"Use the open_file_or_directory tool to open a file, "
                    f"or the create_file_or_directory tool to create one.")

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            total_lines = len(lines)

            # Validate line interval
            start = max(start, 0)
            start = min(start, total_lines + 1)
            end = min(end, total_lines + 1)
            end = max(end, 0)

            # Prepare new content as a list of lines with newline characters
            new_lines = [line if line.endswith('\n') else line + '\n'
                         for line in code.splitlines()]
            old_lines = [line if line.endswith('\n') else line + '\n'
                         for line in lines[start - 1:end]]

            # Replace the target lines
            updated_lines = (
                    lines[:start - 1] +
                    new_lines +
                    lines[end:]
            )
            # Check syntax for the updated file
            updated_lines_code = "\n".join(updated_lines)
            errors = check_syntax(updated_lines_code)

            # Write code to the file
            with open(file_path, 'w') as file:
                file.writelines(updated_lines)
            total_lines = len(updated_lines)
            after = total_lines - end

            # Give feedback about the changes
            response = [f"{i + start}: {line.rstrip()}\n"
                        for i, line in enumerate(old_lines)]
            response += [f"(Changed to)\n"]
            response += [f"{i + start}: {line.rstrip()}\n"
                         for i, line in enumerate(new_lines)]

            if errors:
                # Build response in case of bad code
                response += ["(Code returned to following errors)\n"]
                response += "\n".join(errors) + '\n'

            else:
                # If no errors write the code in the file
                # Format LLM response in case of good code
                response += [f"({after} lines after)\n" if after > 0 else "(end)"]

            header = [f"[File: {self.context.get()} ({total_lines} lines in total)]\n"]
            return "".join(header + response)

        except FileNotFoundError:
            return f"Error: File '{file_path}' not found."
        except Exception as e:
            return f"Error: {e}"