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
                "from": {
                    "type": "number",
                    "description": "The first from the file to be included in the snipped"
                },
                "to": {
                    "type": "number",
                    "description": "Line number until the snippet is shown"
                }
            },
            "required": ["from", "to"],
            "additionalProperties": False
        }
    }
}


def format_snippet(lines, start, end):
    return [f"{i + start}: {line.rstrip()}"
            for i, line in enumerate(lines[start - 1:end])]


def format_header_footer(start, end, total):
    before = start - 1
    after = total - end
    header = f"({before} lines before)" if before > 0 else "(start)"
    footer = f"({after} lines after)" if after > 0 else "(end)"
    return header, footer


def show(start_line: int, end_line: int) -> str:
    try:
        file_path = context.get_abs()
        with open(file_path, "r") as file:
            lines = file.readlines()
        total_lines = len(lines)

        if start_line < 1 or end_line > total_lines or start_line > end_line:
            return (
                f"Error: Invalid line range. The file has {total_lines} lines, "
                f"but received start_line={start_line} and end_line={end_line}."
            )

        snippet = format_snippet(lines, start_line, end_line)
        header, footer = format_header_footer(start_line, end_line, total_lines)
        return "\n".join([header] + snippet + [footer]).strip()

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {e}"