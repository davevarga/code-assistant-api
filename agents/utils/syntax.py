import re
from pathlib import Path


def _detect_indent_char(lines, index):
    line = lines[index]
    if line.startswith("\t"):
        return '\t' # Tabs
    else:
        return ' ' * 4 # Default is spaces


def _get_indentation_level(lines, index, indent_char):
    if index == 0: return 0
    assert index > 0, "Index out of range"

    # Find out indentation at previous line
    line = lines[index - 1]
    pure_code = line.lstrip()
    white_space = line.replace(pure_code, '', 1)
    indentation_level = white_space.count(indent_char)

    # If starts with keyword
    if pure_code.strip().endswith(":"):
        indentation_level += 1
    return indentation_level


class CodeFormatter:
    def __init__(self):
        self.indentation_level = 0
        self.indentation_string = "    "  # 4 spaces

    def insert(self, file: (Path, str), index: int, code: str):
        # Checks should have been handled in the caller function
        file = Path(file) if type(file) == str else file
        assert file.exists(), "File does not exist"
        assert file.suffix == ".py", "File is not a Python file"

        # Skip insertion if code is empty or whitespace
        if not code.strip(): return

        code_lines_from_file = file.read_text().splitlines(keepends=True)
        assert index <= len(code_lines_from_file), f"Line number is out of range: {index} > {len(code_lines_from_file)}"
        assert index >= 0, "Line number is out of range: {index} < 0"

        # Normalize the pro vided code
        code_lines_from_llm = code.splitlines(keepends=True)
        _llm_indent_char = _detect_indent_char(code_lines_from_llm, 0)
        _llm_indentation_level = _get_indentation_level(code_lines_from_llm, index, _llm_indent_char)
        for _index, line in enumerate(code_lines_from_llm):
            line = line.replace(_llm_indent_char * _llm_indentation_level, '', 1)
            code_lines_from_llm[_index] = line

        # Get the indentation level based on the previous code line
        _file_indent_char = _detect_indent_char(code_lines_from_file, index)

        _file_indentation_level = _get_indentation_level(code_lines_from_file[index-1], _file_indent_char)
        for _index, line in enumerate(code_lines_from_llm):
            line = _file_indentation_level * _file_indent_char + line
            code_lines_from_llm[_index] = line

        # Format the correct concatanation
        code_lines_from_file[-1] += '\n'
        code_lines_from_llm[-1] += '\n'
        new_lines = (
            code_lines_from_file[:index] +
            code_lines_from_llm +
            code_lines_from_file[index:]
        )
        file.write_text("".join(new_lines))




