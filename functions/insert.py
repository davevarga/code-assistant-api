from llm import context

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
                "line_number": {
                    "type": "number",
                    "description": "The line before which the code will be inserted"
                },
                "code": {
                    "type": "string",
                    "description": "The python code to be inserted"
                }
            },
            "required": ["from", "to"],
            "additionalProperties": False
        }
    }
}


def insert(line_number: int, code: str) -> str:
    file_path = context.get_abs()
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        total_lines = len(lines)

        # Validate line number
        if line_number < 0 or line_number > total_lines + 1:
            return f"Error: Invalid line number. The file has {total_lines} lines, but received line_number={line_number}."

        # Insert the new code at the correct position
        lines.insert(line_number, code + "\n")

        # Write the modified content back to the file
        with open(file_path, "w") as file:
            file.writelines(lines)

        return f"Success: Code inserted at line {line_number}."

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {str(e)}"