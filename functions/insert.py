from llm import context, check_syntax

# A function that inserts code at a specified line in a file.
# It ensures that the insertion index is valid
# and provides an error message if it's out of bounds.
insert_tool = {
    "type": "function",
    "function": {
        "name": "insert",
        "description": "Inserts the given code at the specified line in the file."
                       "Used to create a new function or class or add a new statement."
                       "Try to use multiple insert calls instead of just a big one."
                       "Keep in mind that the code line numbering will change by adding code to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "number",
                    "description": "The line before which the code will be inserted"
                },
                "code": {
                    "type": "string",
                    "description": "The python code to be inserted"
                }
            },
            "required": ["start", "code"],
            "additionalProperties": False
        }
    }
}


def insert(start: int, code: str) -> str:
    file_path = context.get_abs()
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        total_lines = len(lines)

        # Validate line interval
        start = max(start, 1)
        start = min(start, total_lines - 1)

        # Insert the new code at the correct position
        lines.insert(start, code + "\n")
        code_lines = code.splitlines()

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