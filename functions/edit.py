def insert_code_at_line(file_path: str, line_number: int, code: str) -> str:
    """
    Inserts the given code at the specified line in the file.

    :param file_path: Path to the file where code should be inserted.
    :param line_number: The line index (1-based) where the code should be inserted.
    :param code: The code content to insert.
    :return: A success message or an error message if something goes wrong.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        total_lines = len(lines)

        # Validate line number
        if line_number < 1 or line_number > total_lines + 1:
            return f"Error: Invalid line number. The file has {total_lines} lines, but received line_number={line_number}."

        # Insert the new code at the correct position
        lines.insert(line_number - 1, code + "\n")

        # Write the modified content back to the file
        with open(file_path, "w") as file:
            file.writelines(lines)

        return f"Success: Code inserted at line {line_number}."

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {str(e)}"