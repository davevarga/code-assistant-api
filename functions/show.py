def extract_code_snippet(file_path: str, start_line: int, end_line: int) -> str:
    """
    Extracts and formats a snippet of code from a file, numbering each line.
    The output includes the number of lines before and after the snippet for context.
    If invalid line numbers are given, an explicit error message is returned.

    :param file_path: Path to the Python file.
    :param start_line: The starting line number (1-based index).
    :param end_line: The ending line number (1-based index).
    :return: A formatted string containing the numbered snippet with context info or an error message.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        total_lines = len(lines)

        # Validate line range
        if start_line < 1 or end_line > total_lines or start_line > end_line:
            return f"Error: Invalid line range. The file has {total_lines} lines, but received start_line={start_line} and end_line={end_line}."

        before_count = start_line - 1
        after_count = total_lines - end_line

        # Extract snippet and number lines artificially
        snippet = [f"{i+start_line}: {line.rstrip()}" for i, line in enumerate(lines[start_line - 1 : end_line])]

        # Construct final output
        output = []
        output.append(f"({before_count} lines before)" if before_count > 0 else "(start)")
        output.extend(snippet)
        output.append(f"({after_count} lines after)" if after_count > 0 else "(end)")

        return "\n".join(output).strip()

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {str(e)}"


print(extract_code_snippet("show.py", 20, 30))