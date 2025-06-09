import pytest
from create import CreateTool
from legacy.utils import ContextManager


class TestCreateTool(object):
    @pytest.fixture
    def tool(self, tmp_path):
        self.context = ContextManager(tmp_path)
        return CreateTool(self.context)

    def test_create_directory(self, tool):
        feedback = tool.forward('directory')
        assert tool.context == self.context
        assert tool.context.get().exists()
        assert feedback == f"directory created successfully"
        directory_path = tool.context.get() / 'directory'
        assert directory_path.exists()
        assert directory_path.is_dir()

    def test_create_file(self, tool):
        feedback = tool.forward('file.py')
        assert feedback == "file.py created successfully"
        assert tool.context == self.context
        assert tool.context.get().exists()
        file_path = tool.context.get() / 'file.py'
        assert file_path.exists()
        assert file_path.is_file()

    def test_create_already_existing(self, tool):
        context_path = tool.context.get()
        assert context_path.exists()

        tool.forward('directory')
        feedback = tool.forward('directory')
        directory_path = tool.context.get() / 'directory'
        assert feedback == f"File or directory already exists"
        assert context_path == self.context.get()
        assert directory_path.exists()
        assert len(list(context_path.iterdir())) == 1



