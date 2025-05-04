import os
from smolagents import tool
from utils import context, check_syntax


@tool
def edit_file(start: int, end: int, code: str) -> str:
    """
    Changes the code lines in the given interval, to the given code,
    in the code file that was last opened.
    Args:
        start (int): The beginning of the snippet. The first line number is 1.
        end (int): The number of the last line to be replaced.
        code (str): Python code to be inserted. Line indentation is important.
    Returns:
        str: Feedback based on the outcome of the edit. Provides insight
        into which lines where replaced by what code.
    """
    # Chech if in a file
    file_path = context.get_abs()
    if os.path.isdir(file_path):
        return (f"You are currently in {context.get()} directory. "
                f"Use the open_file_or_directory tool to open a file, "
                f"or the create_file_or_directory tool to create one.")

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        total_lines = len(lines)

        # Validate line interval
        start = max(start, 1)
        start = min(start, total_lines - 1)
        end = min(end, total_lines - 1)
        end = max(end, 1)

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

        header = [f"[File: {context.get()} ({total_lines} lines in total)]\n"]
        return "".join(header + response)

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {e}"