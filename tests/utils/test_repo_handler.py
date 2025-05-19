import shutil

import git
import os
import pytest

from utils import RepoHandler, repo_handler, ContextManager


class TestRepoHandler(object):
    TEMP_DIR = "./temp"
    GITHUB_URL = f"https://github.com/kenshoo/python-style-guide.git"
    REPO_NAME = 'kenshoo/python-style-guide'
    COMMIT_HASH = 'f8d6514'

    @pytest.fixture
    def repo_handler(self, tmp_path):
        tmp_path = tmp_path / "repos"
        tmp_path.mkdir()
        context_handler = ContextManager(tmp_path)
        return RepoHandler(tmp_path, context_handler)

    # Test cloning
    def test_clone(self, repo_handler):
        path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
            TestRepoHandler.COMMIT_HASH,
        )
        assert path, f"Did not return repository path"
        assert os.path.exists(path)
        assert len(os.listdir(path)) != 0, f"Repository is empty"

    def test_clone_without_commit(self, repo_handler):
        path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
        )
        assert path, f"Did not return repository path"
        assert os.path.exists(path)
        assert len(os.listdir(path)) != 0, f"Repository is empty"

    def test_already_cloned_repo(self, repo_handler):
        first_path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
            TestRepoHandler.COMMIT_HASH,
        )
        size_before = len(os.listdir(first_path))
        second_path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
            TestRepoHandler.COMMIT_HASH,
        )
        size_after = len(os.listdir(second_path))
        assert first_path, f"Did not return first repository path"
        assert second_path, f"Did not return second repository path"
        assert first_path == second_path, f"Did not return first repository path"
        assert size_after == size_before, f"Duplicate repository found"

    def test_repo_doesnt_exist(self, repo_handler):
        name = 'doesnt/exist'
        with pytest.raises(
            RuntimeError,
            match=f"Could not clone repository: https://github.com/{name}.git"
        ):
            path = repo_handler.clone(name)
            assert not path, f"Did not clone repository"


    # Test if differences are made if there are no changes
    def test_diff_without_change(self, repo_handler):
        path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
            TestRepoHandler.COMMIT_HASH,
        )
        assert path, f"Did not clone the repository"
        diff = repo_handler.diff()
        assert not diff, f"Diff file should be empty upon initialization"

    def test_diff_with_change(self, repo_handler):
        path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
            TestRepoHandler.COMMIT_HASH,
        )
        assert path, f"Did not clone the repository"
        new_file = os.path.join(path, 'test_diff_with_change.py')
        with open(new_file, 'w') as file:
            file.write("# File created for test purposes")
        diff = repo_handler.diff()
        assert diff, f"Diff should not be empty."

    def test_diff_no_repo(self, repo_handler):
        with pytest.raises(
            RuntimeError,
            match="Repository was not initialized",
        ):
            diff = repo_handler.diff()
            assert not diff, f"Diff exists without a repository"

    def test_delete(self, repo_handler):
        path = repo_handler.clone(
            TestRepoHandler.REPO_NAME,
            TestRepoHandler.COMMIT_HASH,
        )
        assert path, f"Did not clone the repository"
        repo_handler.delete()
        assert not os.path.exists(path), f"Path still exists"
        for index in range(2):
            path = os.path.abspath(os.path.join(path, os.pardir))
            assert not os.path.exists(path), f"Parent still exists"

    def test_delete_without_clonning(self, repo_handler):
        with pytest.raises(
            RuntimeError,
            match="No repository to delete",
        ): repo_handler.delete()
