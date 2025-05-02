import os
import git
import time
import shutil
import stat


def handle_remove_readonly(path: str):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)


class RepoHandler(object):
    def __init__(self, path: str, logger = None):
        self.repo = None
        self.logger = logger
        self.path = path

    def delete(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path, onerror=handle_remove_readonly)

    def clone(self, name: str, commit: str):
        # Derive url from name
        t_start = time.time()
        url = f'https://github.com/{name}.git'
        try:
            # Clone the repository without checking out the HEAD
            self.repo = git.Repo.clone_from(url,self.path,no_checkout=True)
            # Checkout to specific commit
            self.repo.git.checkout(commit)
        except Exception as e:
            print("Valami error: ", e)
        t_end = time.time()

        if self.logger:
            # Log repository cloning
            inference_time = t_end - t_start
            self.logger.log('cloning_time', inference_time)

    def diff(self):
        if self.repo is None:
            # In case of cloning issues skip this repository.
            raise RuntimeError(f'Repository {self.repo} was not initialized')

        # Create the diff file
        return self.repo.git.diff()