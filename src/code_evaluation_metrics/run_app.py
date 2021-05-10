import json
import pathlib
from src.code_evaluation_metrics.entities.repos import GitRepository


def evaluate_repo(repo, tool):
    git_repository = GitRepository(repo, tool)
    git_repository.clone_repo()
    git_repository.get_lines_of_code()
    git_repository.list_tags()
    git_repository.tags_diff()
    git_repository.delete_repo()


def run(json_files_directory, tool):
    for path in pathlib.Path(json_files_directory).iterdir():
        # print("path", path.is_file())
        # if path.is_file():
        # print("path is file", path)
        with open(path) as f:
            repos = json.load(f)
            for repo in repos:
                evaluate_repo(repo, tool)
