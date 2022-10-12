import json
import os
import pathlib
from src.entities.repos import GitRepository

# def get_test_files(repo, tools):
from src.gui.dashboard import dashboard
from src.repo_evaluation_metrics.helpers import back_to_main_dir


def clone_repo(git_repository):
    git_repository.clone_repo()
    return git_repository


def evaluate_repo(git_repository):
    git_repository.create_result_file()
    git_repository.go_to_prj_root()
    git_repository.list_tags()
    git_repository.get_hash_commits()

    git_repository.checkout_last_tag()
    git_repository.get_lines_of_code()
    test_files = git_repository.find_test_files_for_each_tag()

    git_repository.take_metrics_for_each_tag(test_files)

    # TODO: for each tag release read tloc, ploc -> done
    # Then for each tag release calculate tdiff and pdiff -> in progress
    # Then calculate TMR
    #

    # find files that contains test files
    # find files that import those test files
    # count the lines of test code for those files in master branch
    # count for each branch lines of test code and all lines of code
    #
    # git_repository.tags_diff() -> moved to take_metric_function
    # git_repository.calculate_TLR()
    back_to_main_dir()
    print("--------------Done--------------")
    return git_repository


def calculate_TLR(git_repository):
    git_repository.calculate_TLR(git_repository)


def delete_repo(git_repository):
    git_repository.delete_repo()


def run():
    dashboard()
