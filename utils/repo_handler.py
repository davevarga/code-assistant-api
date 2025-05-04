import os
import git
from git.util import rmtree
import shutil
import time


class RepoHandler(object):
    def __init__(self, root: str, logger = None):
        self.repo = None
        self.logger = logger
        self.root = root
        self.path = None

    def delete(self):
        # Because os readonly files Windows might not remove files
        # => git has an integrated deleting mechanism
        self.repo.close()
        rmtree(self.path)

        # Clean up the /repo_owner/repo_name/commit_hash
        os.removedirs(self.root)

    def clone(self, name: str, commit: str):
        # Every repository cloned should have a distinct dir name
        # This is in order to keep accidental conflicts under control
        self.path = os.path.join(self.root, name, commit)
        if os.path.exists(self.path):
            self.repo = git.Repo(self.path)
            return self.path
        try:
            t_start = time.time()
            # Checkout for an explicit commit
            self.repo = git.Repo.clone_from(
                url=f'https://github.com/{name}.git',
                to_path=self.path,
                no_checkout=True
            )
            self.repo.git.checkout(commit)
        except Exception:
            # Skip this repository if it couldn't be opened
            raise RuntimeError(
                f"Could not clone repository: "
                f"https://github.com/{name}.git"
            )
        t_end = time.time()

        if self.logger:
            inference_time = t_end - t_start
            self.logger.log('cloning_time', inference_time)
        return self.path

    def diff(self):
        if self.repo is None:
            # In case of cloning issues skip this repository.
            raise RuntimeError(f'Repository {self.repo} was not initialized')

        # Create the diff file
        return self.repo.git.diff()