import os
import git
import time
from pathlib import Path
from git.util import rmtree

from utils.context_manager import ContextManager
from utils.logger import CSVLogger


class RepoHandler(object):
    def __init__(
            self,
            root: (str, Path),
            context_handler: ContextManager,
            logger: CSVLogger = None
    ):
        self.repo = None
        self.logger = logger
        self.context = context_handler
        self.root = root if type(root) is str else str(root)
        self.path = None
        self.name = None
        self.commit = None

    def delete(self):
        if not self.repo:
            raise RuntimeError(f"No repository to delete")
        assert self.name, f"Repo {self.path} cloned but has no name"
        assert self.commit, f"Repo {self.path} cloned but has no commit"

        # Because os readonly files Windows might not remove files
        # => git has an integrated deleting mechanism
        self.repo.close()
        rmtree(self.path)

        # Clean up the /repo_owner/repo_name/commit_hash temp dirs
        repo_owner = os.path.join(str(self.root), self.name.split("/")[0])
        repo_name = os.path.join(repo_owner, self.name.split("/")[1])

        if not os.listdir(repo_name): os.rmdir(repo_name)
        if not os.listdir(repo_owner): os.rmdir(repo_owner)

    def clone(self, name: str, commit: str = None):
        # Every repository cloned should have a distinct dir name
        # This is in order to keep accidental conflicts under control
        self.name = name
        self.commit = commit if commit else 'HEAD'
        self.path = Path(os.path.join(self.root, name, self.commit))

        if self.path.exists():
            self.repo = git.Repo(self.path)
            self.context.set_root(self.path)
            return self.path
        try:
            t_start = time.time()
            # Checkout for an explicit commit
            self.repo = git.Repo.clone_from(
                to_path=self.path,
                url=f'https://github.com/{self.name}.git',
                no_checkout=True if self.commit else False,
            )
            if self.commit:
                self.repo.git.checkout(self.commit)
            self.context.set_root(self.path)
        # Skip this repository if it couldn't be opened
        except git.exc.GitCommandError:
            raise RuntimeError(
                f"Could not clone repository: "
                f"https://github.com/{self.name}.git"
            )
        except git.exc.GitCommandNotFound as e:
            raise RuntimeError(
                f"Network related error: {e}"
            )
        t_end = time.time()

        if self.logger:
            inference_time = t_end - t_start
            self.logger.log('cloning_time', inference_time)
        return self.path

    def diff(self):
        if self.repo is None:
            # In case of cloning issues skip this repository.
            raise RuntimeError(f"Repository was not initialized")

        # Stage before creating diff file
        self.repo.git.add(A=True)
        return self.repo.git.diff('--cached')

    def repo_path(self, abs: bool = False) -> Path:
        return self.path if abs else self.path.absolute()