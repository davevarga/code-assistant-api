import pytest
from insert import InsertTool
from legacy.utils import ContextManager


class TestInsertTool(object):
    @pytest.fixture
    def create_file(self, tmp_path):
        tmp_path = tmp_path / "file.py"
        tmp_path.touch()
        tmp_path.write_text('import os\n')
        return tmp_path

    @pytest.fixture
    def tool(self, create_file):
        self.context = ContextManager(create_file)
        tool  = InsertTool(self.context)
        return tool

    def test_edit(self, tool):
        file_path = tool.context.get()
        tool.forward(2, 'import tool\n')
        first_line = file_path.read_text()
        assert first_line == "import os\nimport tool\n"


    def test_edit_directory(self, tool):
        tool.context.set_root('..')
        tool.context.set('..')
        directory_path = self.context.get()
        response = tool.forward(1, 'import tool')
        assert response == (
            f"You are cure in {directory_path} directory. "
            f"Use the open_file_or_directory tool to open a file "
            f"or the create_file_or_directory tool to create one."
        )