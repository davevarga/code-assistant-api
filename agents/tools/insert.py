import os
from smolagents import tool
from utils import context, check_syntax


@tool
def insert_code(start: int, code: str) -> str:
    """
    Insert the given code at the specified line number, in the last opened file.
    Args:
        start (int): The line before which the code will be inserted
        code (str): The python code to be inserted
    Returns:
        str: Feedback about the success of the insertion.
    """
    file_path = context.get_abs()
    if os.path.isdir(file_path):
        return (f"You are cure in {context.get()} directory. "
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
        lines.insert(start, code + "\n")
        code_lines = code.splitlines()
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
        header = [f"[File: {context.get()} ({total_lines} lines in total)]\n"]
        return "".join(header + response)

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {str(e)}"