import os
import pytest
from pathlib import Path
from open import OpenTool
from utils import ContextManager, ContextError, ContextPermissionError


class TestOpenTool(object):
    @pytest.fixture
    def tool(self, tmp_path):
        self.context = ContextManager(tmp_path)
        return OpenTool(self.context)

    def test_relative_path(self, tool):
        new_dir = self.context.get() / 'new_dir'
        new_dir.mkdir()
        response = tool.forward('./new_dir')
        assert tool.context.get() == self.context.get()
        assert self.context.get() == new_dir
        assert response == f"Successfully opened {new_dir}"

    def test_absolute_path(self, tool):
        new_dir = self.context.get(abs=True) / 'new_dir'
        new_dir.mkdir()
        response = tool.forward(new_dir.absolute())
        assert tool.context.get() == self.context.get()
        assert self.context.get() == new_dir
        assert response == f"Successfully opened {new_dir}"

    def test_not_existing(self, tool):
        context_before = self.context.get()
        new_dir = "./doesnt/exists"

        response = tool.forward(new_dir)
        assert tool.context.get() == self.context.get()
        assert tool.context.get() == context_before
        assert response == f"File does not exist in {self.context.get()}"

    def test_create_already_existing(self, tool):
        context_before = self.context.get()
        target_dir = '..'

        response = tool.forward(target_dir)
        assert tool.context.get() == self.context.get()
        assert tool.context.get() == context_before
        assert response == f".. permission denied"