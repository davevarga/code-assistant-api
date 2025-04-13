from llm import context

#  Extracts a portion of a Python file, numbers each line,
#  and includes information about how many lines exist before and after the snippet
show_tool = {
    "type": "function",
    "function": {
        "name": "show",
        "description": "Extracts and formats a snippet of code from a file,"
                       "numbering each line. The output includes the number"
                       "of lines before and after the snippet for context",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "number",
                    "description": "The first from the file to be included in the snipped"
                },
                "end": {
                    "type": "number",
                    "description": "Line number until the snippet is shown"
                }
            },
            "required": ["from", "to"],
            "additionalProperties": False
        }
    }
}


def format_response(start, end, lines):
    total = len(lines)
    before = start - 1
    after = total - end

    header = (f"[File: {context.get()} ({total} lines in total)]"
              f"({before} lines before)") if before > 0 else "(start)"
    snippet = [f"{i + start}: {line.rstrip()}"
            for i, line in enumerate(lines[start - 1:end])]
    footer = f"({after} lines after)" if after > 0 else "(end)"

    return "\n".join([header] + snippet + [footer]).strip()


def show(start: int, end: int) -> str:
    file_path = context.get_abs()
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        total_lines = len(lines)

        if start < 1 or end > total_lines or start > end:
            return (
                f"Error: Invalid line range. The file has {total_lines} lines, "
                f"but received start_line={start} and end_line={end}."
            )
        return format_response(start, end, lines)

    except FileNotFoundError:
        return (f"Error: File '{file_path}' not found in current directory."
                f"Use the list function to list all the content")
    except Exception as e:
        return f"Error: {e}"