import pytest
from edit import EditTool
from utils import ContextManager


class TestEditTool(object):
    @pytest.fixture
    def create_file(self, tmp_path):
        tmp_path = tmp_path / "file.py"
        tmp_path.touch()
        tmp_path.write_text('import os')
        return tmp_path

    @pytest.fixture
    def tool(self, create_file):
        self.context = ContextManager(create_file)
        return EditTool(self.context)

    def test_edit(self, tool):
        file_path = tool.context.get()
        tool.forward(1, 1, 'import tool')
        first_line = file_path.read_text()
        assert first_line == "import tool\n"


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