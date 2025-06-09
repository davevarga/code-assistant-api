import pytest
from edit import EditTool
from legacy.utils import ContextManager


PYTHON_CODE ="""def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    if n == 0 or n == 1:
        return 1

    result = n * factorial(n - 1)
    return result
"""


class TestEditTool(object):
    @pytest.fixture
    def create_file(self, tmp_path):
        tmp_path = tmp_path / "file.py"
        tmp_path.write_text(PYTHON_CODE)
        return tmp_path

    @pytest.fixture
    def tool(self, create_file):
        self.context = ContextManager(create_file)
        return EditTool(self.context)

    def test_edit(self, tool):
        file_path = tool.context.get(abs=True)
        tool.forward(1, 2, 'import tool')
        code = file_path.read_text()
        code = code.splitlines()
        assert code[0] == "import tool"
        assert code[1].strip() == """raise ValueError("Factorial is not defined for negative numbers.")"""

    def test_edit_overflow(self, tool):
        file_path = tool.context.get(abs=True)
        tool.forward(20, 20, 'import tool')
        code = file_path.read_text()
        code = code.splitlines()
        assert code[-1] == "import tool"
        assert code[-2].strip() == "return result"

    def test_edit_directory(self, tool):
        tool.context.set_root('..')
        tool.context.set('..')
        directory_path = self.context.get()
        response = tool.forward(1, 1, 'import tool')
        assert response == (
            f"You are currently in {directory_path} directory. "
            f"Use the open_file_or_directory tool to open a file, "
            f"or the create_file_or_directory tool to create one."
        )