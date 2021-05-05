import git


class GitRepository:
    def __init__(self, gitRepo):
        self.git = gitRepo

    def clone_repo(self):
        print(self.git["clone_url"])