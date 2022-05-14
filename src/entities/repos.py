import logging
import os
import json
import subprocess
from git import Git

from src.repo_evaluation_metrics import helpers


class GitRepository:
    def __init__(self, github_repo, tool):
        self.github_repo = github_repo
        self.tool = tool
        self.out_put_file = f"results/repos_statistics/{self.tool}/{self.github_repo['name']}.json"
        self.project_root = f"results/cloned_programs/{github_repo['name']}"
        self.tags = []
        self.TLR = [{}]

    def clone_repo(self):
        try:
            Git("results/cloned_programs").clone(self.github_repo["clone_url"])
            print("clone", self.github_repo["clone_url"])
        except Exception as e:
            logging.info("cloning error:", e)

    def go_to_prj_root(self):
        print("Project root", os.getcwd())
        os.chdir(self.project_root)

    def create_result_file(self):
        repo_name = self.github_repo["name"]
        with open(f"results/repos_statistics/{self.tool}/{repo_name}.json", "w") as outfile:
            json.dump({"repo_name": repo_name}, outfile)

    def append_to_result_file(self, key, value):
        repo_name = self.github_repo["name"]
        try:
            with open(f"../../repos_statistics/{self.tool}/{repo_name}.json", "r+") as outfile:
                # First we load existing data into a dict.
                file_data = json.load(outfile)
                # Join new_data with file_data inside emp_details
                file_data[key] = value
                # Sets file's current position at offset.
                outfile.seek(0)
                # convert back to json.
                json.dump(file_data, outfile, indent=4)
        except Exception as e:
            print("exception:", e)

    def list_tags(self):
        try:
            with open(os.devnull, "w") as fd_devnull:
                subprocess.call(["git", "status", "tags"],
                                stdout=fd_devnull, stderr=fd_devnull)

            cmd = "git tag".split()
            try:
                dirty = subprocess.check_output(cmd).decode().strip()
                self.tags = dirty.splitlines()

            except subprocess.CalledProcessError:
                print("Unable to get git tags")
                exit(1)
        except Exception as e:
            logging.info("list tags error", e)

    def get_lines_of_code(self, tag="master", key_subject="CLOC"):
        try:
            os.system(f"cloc {self.github_repo['name']} --json --out=./cloc.json")
            with open("./cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
                self.append_to_result_file(f"{key_subject}_{tag}", file_data)

        except Exception as e:
            logging.info("cloc lines of code", e)

    def get_lines_of_code_for_test_file(self, tag, file_name):
        path = os.getcwd()
        for root, dirs, files in os.walk(path):
            if file_name in files:
                try:
                    os.system(f"cloc {file_name} --json --out=./cloc.json")
                    with open("./cloc.json", "r+") as outfile:
                        file_data = json.load(outfile)
                        self.append_to_result_file(f"TTL_{tag}", file_data)

                except Exception as e:
                    logging.info("cloc lines of code for test file", e)

    def find_test_files(self):
        result = helpers.do_bash_cmd_return_result_in_array(f"git grep -i --name-only {self.tool}")
        valid_files = []
        if len(result) >= 1:
            for line in result:
                decoded_line = line.decode("utf-8")
                if helpers.check_validation(decoded_line):
                    pure_file_path = decoded_line.strip("\n")
                    valid_files.append(pure_file_path)
                    slash_index = pure_file_path.rfind("/") + 1
                    dot_index = pure_file_path.rfind(".")
                    pure_file_name = pure_file_path[slash_index:dot_index]

                    # find files that import test files
                    files_import_tests = helpers.do_bash_cmd_return_result_in_array(f"git grep -i --name-only {pure_file_name}")

                    if len(files_import_tests) >= 1:
                        for file in files_import_tests:
                            decoded_file_name = file.decode("utf-8")
                            if helpers.check_validation(decoded_file_name):
                                valid_files.append(decoded_file_name)

        return valid_files

    def tags_diff(self):
        try:
            for i in range(len(self.tags) - 1):
                os.chdir(f"./results/cloned_programs/{self.github_repo['name']}")
                git_name = self.github_repo['name']
                os.system(
                    f"cloc --git --diff {self.tags[i]} {self.tags[i + 1]} --csv --out=../../csv/{self.tool}/{git_name}/{self.tags[i]}_{self.tags[i + 1]}")
                os.chdir("../..")

        except Exception as e:
            logging.info("tags different", e)

    def save_TLR_metrics(self, test_files):
        # For each tag, in self.tags:
        # 1- Save cloc TTLi
        # 2- Save PLOCi
        for tag in self.tags:
            Git(os.getcwd()).checkout(tag)
            self.get_lines_of_code(tag, "PLOC")
            for file in test_files:
                self.get_lines_of_code_for_test_file(tag, file)

    def delete_repo(self):
        os.system(f"rm -rf ./results/cloned_programs/{self.github_repo['name']}")
