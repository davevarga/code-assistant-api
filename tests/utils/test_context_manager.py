import os
import pytest

from utils import ContextManager, ContextError, ContextPermissionError


class TestContextManager(object):
    def test_init_with_root(self, tmp_path):
        context_manager = ContextManager(tmp_path)
        assert context_manager, f"Creating context manager failed"
        assert context_manager.root == tmp_path

    def test_init_with_non_existing_root(self, tmp_path):
        tmp_path = tmp_path / 'non_existing_root'
        with pytest.raises(ContextError):
            context_manager = ContextManager(tmp_path)
            assert not context_manager.root, f"Root still exists"

    def test_init_with_root_and_cwd(self, tmp_path):
        current_path = tmp_path / 'test'
        current_path.mkdir()
        context_manager = ContextManager(tmp_path, current_path)

        assert context_manager, f"Creating context manager failed"
        assert context_manager.root == tmp_path
        assert context_manager.cwd == current_path

    def test_init_cwd_outside_root(self, tmp_path):
        current_path = tmp_path
        root_path = tmp_path / 'root'
        root_path.mkdir()
        with pytest.raises(ContextPermissionError):
            ContextManager(root_path, current_path)

    def test_set_context(self, tmp_path):
        root_path = tmp_path
        context_manager = ContextManager(root_path)
        assert context_manager.root == root_path
        assert context_manager.cwd == root_path

        new_path = tmp_path / 'new_path'
        new_path.mkdir()
        context_manager.set(new_path)
        assert context_manager.root == root_path
        assert context_manager.cwd == new_path

    def test_set_context_outside_root(self, tmp_path):
        root_path = tmp_path
        current_path = tmp_path / 'test'
        current_path.mkdir()
        context_manager = ContextManager(root_path, current_path)
        assert context_manager.root == root_path
        assert context_manager.cwd == current_path

        new_path = tmp_path / '..'
        with pytest.raises(ContextPermissionError):
            context_manager.set(new_path)
        assert context_manager.cwd == current_path

        new_path = 'valamit/uj'
        with pytest.raises(ContextError):
            context_manager.set(new_path)
        assert context_manager.cwd == current_path

    def test_get_context(self, tmp_path):
        root_path = tmp_path
        current = tmp_path / 'get'
        current.mkdir()
        context_manager = ContextManager(root_path, current)
        assert context_manager.root == root_path
        assert context_manager.cwd == current
        assert context_manager.get() == current

    def test_set_root(self, tmp_path):
        root_path = tmp_path
        current_path = tmp_path / 'test'
        current_path.mkdir()
        context_manager = ContextManager(root_path, current_path)
        assert context_manager.root == root_path
        assert context_manager.cwd == current_path

        old_root = tmp_path / 'test'
        context_manager.set_root(old_root)
        assert context_manager.root == old_root
        assert context_manager.cwd == current_path

        new_root = tmp_path / 'new_path'
        with pytest.raises(ContextError):
            context_manager.set_root(new_root)
        assert context_manager.root == old_root
        assert context_manager.cwd == current_path

        new_root = tmp_path / 'test' / 'new_path'
        new_root.mkdir()
        context_manager.set_root(new_root)
        assert context_manager.root == new_root
        assert context_manager.cwd == new_root