import json
import pathlib
from src.entities.repos import GitRepository, back_to_main_dir

#
# def get_test_files(repo, tools):



def evaluate_repo(repo, tool):
    git_repository = GitRepository(repo, tool)
    git_repository.create_result_file()
    git_repository.clone_repo()
    git_repository.go_to_prj_root()
    git_repository.get_lines_of_code()


    #find files that contains test files
    #find files that import those test files
    #count the lines of test code for those files in master branch
    #count for each branch lines of test code and all lines of code

    # git_repository.list_tags()
    # git_repository.tags_diff()
    # git_repository.delete_repo()
    back_to_main_dir()


def run(json_files_directory, tool):
    for path in pathlib.Path(json_files_directory).iterdir():
        # print("path", path.is_file())
        # if path.is_file():
        # print("path is file", path)
        with open(path) as f:
            repos = json.load(f)
            for repo in repos:
                evaluate_repo(repo, tool)
