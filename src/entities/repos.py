import logging
import os
import json
import csv
import subprocess
import git


def back_to_main_dir():
    return os.chdir("../../..")


def do_bash_cmd_return_result_in_array(command):
    proc = subprocess.Popen([command],
                            shell=True,
                            stdin=None,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    return proc.stdout.readlines()

def check_validation(decoded_line):
    ".json" not in decoded_line and ".md" not in decoded_line \
    and ".npmignore" not in decoded_line \
    and ".gitignore" not in decoded_line \
    and ".yml" not in decoded_line


class GitRepository:
    def __init__(self, github_repo, tool):
        self.github_repo = github_repo
        self.tool = tool
        self.project_root = f"results/cloned_programs/{github_repo['name']}"
        self.tags = []

    def clone_repo(self):
        try:
            git.Git("results/cloned_programs").clone(self.github_repo["clone_url"])
            print("clone", self.github_repo["clone_url"])
        except Exception as e:
            logging.info("cloning error:", e)

    def go_to_prj_root(self):
        os.chdir(self.project_root)

    def create_result_file(self):
        repo_name = self.github_repo["name"]
        with open(f"results/repos_statistics/selenium/{repo_name}.json", "w") as outfile:
            json.dump({"repo_name": repo_name}, outfile)

    def append_to_result_file(self, key, value):
        repo_name = self.github_repo["name"]
        with open(f"results/repos_statistics/selenium/{repo_name}.json", "r+") as outfile:
            # First we load existing data into a dict.
            file_data = json.load(outfile)
            # Join new_data with file_data inside emp_details
            file_data[key] = value
            # Sets file's current position at offset.
            outfile.seek(0)
            # convert back to json.
            json.dump(file_data, outfile, indent=4)

    def list_tags(self):
        try:
            self.tags = git.Repo(self.project_root).tags
        except Exception as e:
            logging.info("list tags error", e)

    def get_lines_of_code(self):
        try:
            # proc = subprocess.Popen([f"cloc {self.github_repo['name']} --json --out="], stdout=subprocess.PIPE, shell=True)
            # (out, err) = proc.communicate()
            # self.append_to_result_file("LOC", out)

            # os.chdir("./results/cloned_programs")
            # git_name = self.github_repo['name']
            os.system(f"cloc {self.github_repo['name']} --json --out=./cloc.json")
            # os.chdir("..")
            with open("./cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
                self.append_to_result_file("cloc", file_data)

            # print("current dir", os.getcwd())
            # with open(f"csv/self.github_repo['name']", "w", newline="") as csvfile:
            # with open("csv/workbox", 'w', newline='\n') as csvfile:
            #     loc = csv.writer(csvfile, delimiter=' ',
            #                      quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            #     loc.writerow("TOTAL LOC")
            #     loc.writerow(cloc)

        except Exception as e:
            logging.info("cloc lines of code", e)

    def find_test_files(self):
        result = do_bash_cmd_return_result_in_array(f"git grep -i --name-only {self.tool}")
        valid_files = []
        if len(result) >= 1:
            for line in result:
                decoded_line = line.decode("utf-8")

                if check_validation(decoded_line):
                    pure_file_path = decoded_line.strip("\n")
                    valid_files.append(pure_file_path)
                    slash_index = pure_file_path.rfind("/") + 1
                    dot_index = pure_file_path.rfind(".")
                    pure_file_name = pure_file_path[slash_index:dot_index]
                    files_import_tests = do_bash_cmd_return_result_in_array(f"git grep -i --name-only {pure_file_name}")
                    if len(files_import_tests) >= 1:
                        for file in files_import_tests:
                            decoded_file_name = file.decode("utf-8")
                            if check_validation(decoded_file_name):
                                print(">>>>>>>>>>>>>>>>>>>>>")
                                print(decoded_file_name)
    #                           //to do check correctness


    def tags_diff(self):
        try:
            for i in range(len(self.tags) - 1):
                os.chdir(f"./results/cloned_programs/{self.github_repo['name']}")
                # print("current dir", os.getcwd())
                git_name = self.github_repo['name']
                os.system(
                    f"cloc --git --diff {self.tags[i]} {self.tags[i + 1]} --csv --out=../../csv/{self.tool}/{git_name}/{self.tags[i]}_{self.tags[i + 1]}")
                os.chdir("../..")

        except Exception as e:
            logging.info("tags different", e)

    def delete_repo(self):
        os.chdir("./results/cloned_programs")
        os.system(f"rm -rf {self.github_repo['name']}")
        os.chdir("..")
