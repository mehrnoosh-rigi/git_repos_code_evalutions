import json
import os
import pathlib
from src.entities.repos import GitRepository

# def get_test_files(repo, tools):
from src.repo_evaluation_metrics.helpers import back_to_main_dir


def evaluate_repo(repo, tool):
    git_repository = GitRepository(repo, tool)
    git_repository.create_result_file()
    git_repository.clone_repo()
    git_repository.go_to_prj_root()
    git_repository.list_tags()
    git_repository.get_lines_of_code()
    test_files = git_repository.find_test_files()
    git_repository.save_TLR_metrics(test_files)

    # find files that contains test files
    # find files that import those test files
    # count the lines of test code for those files in master branch
    # count for each branch lines of test code and all lines of code

    git_repository.tags_diff()
    back_to_main_dir()
    git_repository.delete_repo()


def run(json_files_directory, tool):
    for path in pathlib.Path(json_files_directory).iterdir():
        # print("path", path.is_file())
        if path.is_file():
            print("path is file", path)
        with open(path) as f:
            repos = json.load(f)
            for repo in repos:
                evaluate_repo(repo, tool)
