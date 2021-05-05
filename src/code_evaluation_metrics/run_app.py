import json
import pathlib
from src.code_evaluation_metrics.entities.repos import GitRepository


def evaluate_repo(repo):
    git_repository = GitRepository(repo)
    git_repository.clone_repo()


def run(json_files_directory):
    for path in pathlib.Path(json_files_directory).iterdir():
        if path.is_file():
            with open(path) as f:
                repos = json.load(f)
                for repo in repos:
                    evaluate_repo(repo)
