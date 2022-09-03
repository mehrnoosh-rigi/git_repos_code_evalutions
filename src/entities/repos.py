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
        """
        clone the repository from the result file
        """
        try:
            Git("results/cloned_programs").clone(self.github_repo["clone_url"])
            print("clone", self.github_repo["clone_url"])
        except Exception as e:
            print("cloning error:", e)

    def go_to_prj_root(self):
        """
        change the directory of project to the cloned program
        """
        os.chdir(self.project_root)
        print("Directory changed to:", os.getcwd())

    def create_result_file(self):
        """
        Create a result file as a Json file
        """
        repo_name = self.github_repo["name"]
        with open(f"results/repos_statistics/{self.tool}/{repo_name}.json", "w") as outfile:
            data = {'repo_name': repo_name}
            json.dump(data, outfile)

    def append_to_result_file(self, key, value):
        """
        Append to the result file
        :param key: is the Key of object
        :param value: is the value of object
        """
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
            print("Error in appending to the result file", e)

    def checkout_last_tag(self):
        """
        Put the head of git in the last tag commit
        """
        Git(os.getcwd()).checkout(self.tags[len(self.tags) - 1])

    def list_tags(self):
        """
        List all tags of the current git repository
        """
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
            print("list tags error", e)

    def get_lines_of_code(self, tag="master", key_subject="CLOC"):
        """
        get lines of code for the tag
        :param tag: if tag is passed, save tag if not, it's master by default
        :param key_subject: if key_subject is passed it's save as passed value if not it's CLOC by default value
        """
        try:
            os.chdir("../")

            os.system(f"cloc {self.github_repo['name']} "
                      f"--ignore-whitespace "
                      f"--ignore-case "
                      f"--json "
                      f"--out={self.github_repo['name']}/cloc.json")

            os.chdir(f"./{self.github_repo['name']}")

            with open("cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
            self.append_to_result_file(f"{key_subject}_{tag}", file_data)

        except Exception as e:
            print("cloc lines of code", e)

    # def calculate_Tdiff(self, tag, file_data):
    #
    #     self.append_to_result_file(f"Tdiff_{tag}", file_data["header"]["n_lines"])

    def get_lines_of_code_for_test_file(self, tag, file_name):
        path = os.getcwd()
        for root, dirs, files in os.walk(path):
            if file_name in files:
                try:
                    print("file name", file_name)
                    os.system(f"cloc {file_name} --json --out=./cloc.json")
                    with open("./cloc.json", "r+") as outfile:
                        file_data = json.load(outfile)
                        self.append_to_result_file(f"TTL_{tag}", file_data["header"]["n_lines"])
                        # if index > 0:
                        #     self.calculate_Tdiff(tag, file_data)
                except Exception as e:
                    print("cloc lines of code for test file", e)

    def find_test_files_for_each_tag(self):
        """
        Find each files that contains the tool inside, by any Import for each tag release
        Then sanitize files, if it's yml, txt, md or ... files which are not important don't consider them
        Then also find files that import these files
        And at the end return the array of valid files
        """
        try:
            for tag in self.tags:
                Git(os.getcwd()).checkout(tag)
                print("git status::", helpers.do_bash_cmd_return_result_in_array("git status"))
                print("current tag:", tag)
                result = helpers.do_bash_cmd_return_result_in_array(f"git grep -i --name-only {self.tool}")
                valid_files = []
                print("result", result)
                # I am here, it seems the command doesn't return anuthing, I didn't delete repose try to check them
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
                            files_import_tests = helpers.do_bash_cmd_return_result_in_array(
                                f"git grep -i --name-only {pure_file_name}")

                            if len(files_import_tests) >= 1:
                                for file in files_import_tests:
                                    decoded_file_name = file.decode("utf-8")
                                    if helpers.check_validation(decoded_file_name):
                                        print("decoded file name:::::", decoded_file_name)
                                        pure_file_path = decoded_file_name.strip("\n")
                                        valid_files.append(pure_file_path)
                            print("valid files:::::", valid_files)
                return valid_files
        except Exception as err:
            print("error in take file tests", err)

    def tags_diff(self):
        try:
            for i in range(len(self.tags) - 1):
                os.chdir(f"./results/cloned_programs/{self.github_repo['name']}")
                git_name = self.github_repo['name']
                os.system(
                    f"cloc --git --diff {self.tags[i]} {self.tags[i + 1]} --csv --out=../../csv/{self.tool}/{git_name}/{self.tags[i]}_{self.tags[i + 1]}")
                os.chdir("../..")

        except Exception as e:
            print("tags different", e)

    def take_metrics_for_each_tag(self, test_files):
        # For each tag, in self.tags:
        # 1- Save cloc TTLi
        # 2- Save 0913i
        # 3- take Tdiffi
        for index, tag in enumerate(self.tags):
            Git(os.getcwd()).checkout(tag)
            self.get_lines_of_code(tag, "PLOC")
            for file in test_files:
                self.get_lines_of_code_for_test_file(tag, file)
                # TODO: for each tag release read tloc, ploc
                # Then for each tag release calculate tdiff and pdiff
                # Then calculate TMR
                #

    def delete_repo(self):
        os.system(f"rm -rf ./results/cloned_programs/{self.github_repo['name']}")

    def calculate_TLR(self):
        repo_name = self.github_repo["name"]
        with open(f"../../repos_statistics/{self.tool}/{repo_name}.json", "r") as result_file:
            data = json.load(result_file)
            for tag in self.tags:
                try:
                    current_tag_TTL = data[f"TTL_{tag}"]
                    current_tag_PLOC = data[f"PLOC_{tag}"]["header"]["n_lines"]
                    self.append_to_result_file(f"TLR_{tag}", int(current_tag_TTL) / int(current_tag_PLOC))
                except Exception as error:
                    self.append_to_result_file(f"TLR_{tag}", 0)
                    print("error in TLR calculation", error)
                    pass

    def calculate_MTLR(self):
        repo_name = self.github_repo["name"]
        with open(f"../../repos_statistics/{self.tool}/{repo_name}.json", "r") as result_file:
            data = json.load(result_file)
            for index, tag in enumerate(self.tags):
                try:
                    if 0 < index < len(self.tags):
                        current_tag_TTL = data[f"TTL_{tag}"]
                        next_tag_TTL = data[f"TTL_{self.tags[index + 1]}"]
                        current_tag_diff = abs(int(next_tag_TTL) - int(current_tag_TTL))
                        self.append_to_result_file(f"TDiff_{tag}", current_tag_diff)
                        # you have computed the tDiff
                        # now you should take the Tloc i
                        # then compute MTLR
                        # then check for other months
                        # if it's always zero something is wrong

                except Exception as error:
                    print("Error in MTLR calculation:", error)
                    pass
