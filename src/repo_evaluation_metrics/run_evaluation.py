import json
import os
import pathlib
from src.entities.repos import GitRepository

# def get_test_files(repo, tools):
from src.gui.dashboard import dashboard
from src.repo_evaluation_metrics.helpers import back_to_main_dir


def evaluate_repo(repo, tool):
    git_repository = GitRepository(repo, tool)
    git_repository.create_result_file()
    git_repository.clone_repo()
    git_repository.go_to_prj_root()
    git_repository.list_tags()
    git_repository.get_lines_of_code()
    test_files = git_repository.find_test_files_for_each_tag()
    git_repository.take_metrics_for_each_tag(test_files)

    # find files that contains test files
    # find files that import those test files
    # count the lines of test code for those files in master branch
    # count for each branch lines of test code and all lines of code

    git_repository.tags_diff()
    git_repository.calculate_TLR()
    back_to_main_dir()
    # git_repository.delete_repo()


def evaluate_file(json_files_directory):
    tool = "selenium" if "selenium" in json_files_directory else "cypress"
    with open(json_files_directory) as f:
        repos = json.load(f)
        for repo in repos:
            evaluate_repo(repo, tool)


def run():
    dashboard()
