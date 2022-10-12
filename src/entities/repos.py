import os
import json
import subprocess
from git import Git
from pathlib import Path

from src.repo_evaluation_metrics import helpers

TTli = 0
Tdiffi = 0


def find_files_that_import_test_file(folders, valid_files):
    try:
        for line in folders:
            # Remove unnecessary files and take pure file name
            decoded_line = line.decode("utf-8")
            if helpers.check_validation(decoded_line):
                pure_file_path = decoded_line.strip("\n")
                valid_files.append(pure_file_path)
                slash_index = pure_file_path.rfind("/")
                dot_index = pure_file_path.rfind(".")
                pure_file_name = os.path.basename(pure_file_path)

                # find files that import test files
                files_import_tests = helpers.do_bash_cmd_return_result_in_array(
                    f"git grep -i --name-only {pure_file_name}")

                if len(files_import_tests) >= 1:
                    for file in files_import_tests:
                        decoded_file_name = file.decode("utf-8")
                        if helpers.check_validation(decoded_file_name):
                            pure_file_path = decoded_file_name.strip("\n")
                            valid_files.append(pure_file_path)
        return valid_files
    except Exception as error:
        print("Error in find files which import test files", error)


def find_test_directory_for_each_tag():
    try:
        result = helpers.do_bash_cmd_return_result_in_array("git ls-files | xargs -n 1 dirname | uniq")

        test_folders = list(filter(lambda folder: ("test" in str(folder)), result))
        valid_files = []
        return find_files_that_import_test_file(test_folders, valid_files)

    except Exception as error:
        print(f"Error in find text directory {error}")


def get_lines_of_code_for_test_file(file_path):
    path = os.getcwd()
    file_name = os.path.basename(file_path)
    for root, dirs, files in os.walk(path):
        if file_name in files:
            try:
                os.system(f"cloc {file_path} --json --out=./cloc.json")
                with open("./cloc.json", "r+") as outfile:
                    file_data = json.load(outfile)
                    global TTli
                    TTli = file_data["header"]["n_lines"] + TTli
                    # if index > 0:
                    #     self.calculate_Tdiff(tag, file_data)
            except Exception as e:
                print("Cloc lines of code for test file", e)

    return TTli


class GitRepository:
    def __init__(self, github_repo, tool):
        self.github_repo = github_repo
        self.tool = tool
        self.out_put_file = f"results/repos_statistics/{self.tool}/{self.github_repo['name']}.json"
        self.project_root = f"results/cloned_programs/{github_repo['name']}"
        self.tags = []
        self.hash_commits = []

    def clone_repo(self):
        """
        clone the repository from the result file
        """
        try:
            Git("results/cloned_programs").clone(self.github_repo["clone_url"])
            print("Cloned", self.github_repo["clone_url"])
        except Exception as e:
            print("Cloning error:", e)

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
            print("Error in appending to the result file", e, key, value)

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
                self.append_to_result_file("NTR", len(self.tags))
            except subprocess.CalledProcessError:
                print("Unable to get git tags")
                exit(1)
        except Exception as e:
            print("List tags error", e)

    def get_hash_commits(self):
        for tag in self.tags:
            current_hash_commit = helpers.do_bash_cmd_return_result_in_array(f"git rev-list -n 1 tags/{tag}")[0]
            self.hash_commits.append(current_hash_commit.decode("ascii").replace("\n", ""))

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
            self.append_to_result_file(f"{key_subject}_{tag}", file_data["header"]["n_lines"])

        except Exception as e:
            print("Cloc lines of code", e)

    # def calculate_Tdiff(self, tag, file_data):
    #
    #     self.append_to_result_file(f"Tdiff_{tag}", file_data["header"]["n_lines"])

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
                result = helpers.do_bash_cmd_return_result_in_array(f"git grep -i --name-only {self.tool}")
                valid_files = find_test_directory_for_each_tag()
                if len(result) >= 1:
                    # Remove unnecessary files and take pure file name
                    valid_files = find_files_that_import_test_file(result, valid_files)

            return valid_files
        except Exception as err:
            print("Error in take file tests", err)

    def tool_tags_diff_LOC(self, index, file_path):
        """
        :param file_path: test file
        :param index: tag index
        :return: Save to result file for each tag the tags differences between i and i-1
        """
        try:
            global current_tag_LOC, prev_tag_LOC
            current_tag_LOC = 0
            prev_tag_LOC = 0
            os.system(f"cloc {file_path} --json --out=./cloc.json")

            with open("./cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
                print("file data>>>>", file_data)
                test_file_LOC = file_data["SUM"]["code"]
                current_tag_LOC = test_file_LOC

            Git(os.getcwd()).checkout(self.tags[index - 1])
            os.system(f"cloc {file_path} --json --out=./cloc.json")
            with open("./cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
                test_file_LOC = file_data["SUM"]["code"]
                prev_tag_LOC = test_file_LOC
                file_name = os.path.basename(file_path)
                global Tdiffi
                Tdiffi = int(current_tag_LOC) - int(prev_tag_LOC)
                self.append_to_result_file(f"Tdiff-{self.tags[index]}-{self.tags[index - 1]}-{file_name}-{index}",
                                           Tdiffi)

            Git(os.getcwd()).checkout(self.tags[index])

        except Exception as e:
            print("Tool tags different error", e)

    def production_lines_of_code_tags_diff(self, index):
        """
        :param file_path: test file
        :param index: tag index
        :return: Save to result file for each tag the tags differences between i and i-1
        """
        try:
            global PLOC_current_LOC, prev_PLOC_current_LOC
            PLOC_current_LOC = 0
            prev_PLOC_current_LOC = 0

            os.chdir("../")

            os.system(f"cloc {self.github_repo['name']} "
                      f"--ignore-whitespace "
                      f"--ignore-case "
                      f"--json "
                      f"--out=./cloc.json")

            os.chdir(f"./{self.github_repo['name']}")
            # os.system(f"cloc --json --out=./cloc.json")
            with open("./cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
                test_file_LOC = file_data["SUM"]["code"]
                PLOC_current_LOC = test_file_LOC

            Git(os.getcwd()).checkout(self.tags[index - 1])
            # os.system(f"cloc --json --out=./cloc.json")
            os.chdir("../")

            os.system(f"cloc {self.github_repo['name']} "
                      f"--ignore-whitespace "
                      f"--ignore-case "
                      f"--json "
                      f"--out=./cloc.json")

            os.chdir(f"./{self.github_repo['name']}")
            with open("./cloc.json", "r+") as outfile:
                file_data = json.load(outfile)
                test_file_LOC = file_data["SUM"]["code"]
                prev_PLOC_current_LOC = test_file_LOC
                global pdiffi
                pdiffi = int(PLOC_current_LOC) - int(prev_PLOC_current_LOC)
                if pdiffi == 0:
                    pdiffi = prev_PLOC_current_LOC
                self.append_to_result_file(f"Pdiff-{self.tags[index]}-{self.tags[index - 1]}_{index}",
                                           pdiffi)

            Git(os.getcwd()).checkout(self.tags[index])

        except Exception as e:
            print(f"Production LOC {self.tags[index]} error", e)

    def calculate_TMR(self):
        with open(f"../../repos_statistics/{self.tool}/{self.github_repo['name']}.json", "r") as result_file:
            data = json.load(result_file)
            try:
                MRTL = [v for k, v in data.items() if k.startswith('MRTL')]
                TLR = [v for k, v in data.items() if k.startswith('TLR')]
                for index, tag in enumerate(self.tags):
                    if len(self.tags) - 1 > index > 0:
                        MRTLi = MRTL[index]
                        TLRi_1 = TLR[index - 1]
                        if TLRi_1 == 0:
                            TLRi_1 = 1
                        TMRi = MRTLi / TLRi_1
                        self.append_to_result_file(f"TMR_{tag}_{index}", TMRi)

            except Exception as error:
                self.append_to_result_file(f"TMR_{tag}", 0.0)
                print("error in TMR calculation", error)
                pass

    # def production_lines_of_code_tags_diff(self, index):
    #     """
    #     :param index: tag index
    #     :return: Save to result file for each tag the tool files differences between i and i-1
    #     """
    #     try:
    #         if index < len(self.tags) - 1:
    #             os.system(
    #                 f"cloc --git --diff {self.tags[index]} {self.tags[index + 1]} "
    #                 f"--json --out=./cloc.json")
    #             # os.chdir("../..")
    #             with open("./cloc.json", "r+") as outfile:
    #                 file_data = json.load(outfile)
    #                 self.append_to_result_file(f"Pdiff{index}-{index + 1}", file_data["header"]["n_lines"])
    #
    #     except Exception as e:
    #         print("Production lines of code tags different error", e)

    def take_metrics_for_each_tag(self, test_files):
        # For each tag, in self.tags:
        # 1- Save cloc TTLi
        # 2- Save PLOCi
        # 3- take Tdiffi
        # 4- take Pdiffi
        for index, tag in enumerate(self.tags):
            Git(os.getcwd()).checkout(tag)
            self.get_lines_of_code(tag, "PLOC")  # PLOCi
            global Tdiffi, TTli
            Tdiffi = 0
            TTli = 0
            TTLOC = 0
            for file in test_files:
                # it should calculate for each tag all results
                TTLi = get_lines_of_code_for_test_file(file) + TTli  # TTLi
                self.append_to_result_file(f"TTL_{tag}", TTLi)

                if index > 0:
                    self.tool_tags_diff_LOC(index, file)  # TDIFFi, i+1
                    # self.tool_tags_diff(index, file)
                    # self.append_to_result_file(f"Tdiff-{self.tags[index]}-{self.tags[index - 1]}",
                    #                            TTLOC)
            self.production_lines_of_code_tags_diff(index)  # PDIFFi, i-1

            # self.production_lines_of_code_tags_diff(index)  # PDIFFi, i+1
        self.calculate_TLR()
        self.calculate_MTLR()
        self.calculate_MRTL()
        self.calculate_TMR()

    def delete_repo(self):
        os.system(f"rm -rf ./results/cloned_programs/{self.github_repo['name']}")

    def calculate_TLR(self):
        with open(f"../../repos_statistics/{self.tool}/{self.github_repo['name']}.json", "r") as result_file:
            data = json.load(result_file)
            try:
                TTLs = [v for k, v in data.items() if k.startswith('TTL')]
                PLOCs = [v for k, v in data.items() if k.startswith('PLOC')]
                for index, tag in enumerate(self.tags):
                    TLRi = TTLs[index] / PLOCs[index]
                    self.append_to_result_file(f"TLR_{tag}_{index}", TLRi)

            except Exception as error:
                self.append_to_result_file(f"TLR_{tag}", 0)
                print("error in TLR calculation", error)
                pass

    def calculate_MTLR(self):
        with open(f"../../repos_statistics/{self.tool}/{self.github_repo['name']}.json", "r") as result_file:
            data = json.load(result_file)
            try:
                Tdiff = [v for k, v in data.items() if k.startswith('Tdiff')]
                TTLs = [v for k, v in data.items() if k.startswith('TTL')]
                print("Tdiff i>>", Tdiff)
                print("TTLs >>", TTLs)
                for index, tag in enumerate(self.tags):
                    if len(self.tags) - 1 > index > 0:
                        MTLRi = Tdiff[index] / TTLs[index - 1]
                        self.append_to_result_file(f"MTLR_{tag}_{index}", MTLRi)

            except Exception as error:
                self.append_to_result_file(f"MTLR_{tag}", 0)
                print("error in MTLR calculation", error)
                pass
        #
        # repo_name = self.github_repo["name"]
        # with open(f"../../repos_statistics/{self.tool}/{repo_name}.json", "r") as result_file:
        #     data = json.load(result_file)
        #     for index, tag in enumerate(self.tags):
        #         try:
        #             if 0 < index < len(self.tags):
        #                 current_tag_TTL = data[f"TTL_{tag}"]
        #                 next_tag_TTL = data[f"TTL_{self.tags[index + 1]}"]
        #                 current_tag_diff = abs(int(next_tag_TTL) - int(current_tag_TTL))
        #                 self.append_to_result_file(f"TDiff_{tag}", current_tag_diff)
        #                 # you have computed the tDiff
        #                 # now you should take the Tloc i
        #                 # then compute MTLR
        #                 # then check for other months
        #                 # if it's always zero something is wrong
        #
        #         except Exception as error:
        #             print("Error in MTLR calculation:", error)
        #             pass

    def calculate_MRTL(self):
        with open(f"../../repos_statistics/{self.tool}/{self.github_repo['name']}.json", "r") as result_file:
            data = json.load(result_file)
            try:
                Tdiff = [v for k, v in data.items() if k.startswith('Tdiff')]
                Pdiff = [v for k, v in data.items() if k.startswith('Pdiff')]
                print("Tdiff i>>", Tdiff)
                print("TTLs >>", Pdiff)
                for index, tag in enumerate(self.tags):
                    if len(self.tags) - 1 > index > 0:
                        MRTLi = Tdiff[index] / Pdiff[index - 1]
                        self.append_to_result_file(f"MRTL_{tag}_{index}", MRTLi)

            except Exception as error:
                self.append_to_result_file(f"MRTL_{tag}", 0)
                print("error in MRTL calculation", error)
                pass
        #
        # repo_name = self.github_repo["name"]
        # with open(f"../../repos_statistics/{self.tool}/{repo_name}.json", "r") as result_file:
        #     data = json.load(result_file)
        #     for index, tag in enumerate(self.tags):
        #         try:
        #             if 0 < index < len(self.tags):
        #                 current_tag_TTL = data[f"TTL_{tag}"]
        #                 next_tag_TTL = data[f"TTL_{self.tags[index + 1]}"]
        #                 current_tag_diff = abs(int(next_tag_TTL) - int(current_tag_TTL))
        #                 self.append_to_result_file(f"TDiff_{tag}", current_tag_diff)
        #                 # you have computed the tDiff
        #                 # now you should take the Tloc i
        #                 # then compute MTLR
        #                 # then check for other months
        #                 # if it's always zero something is wrong
        #
        #         except Exception as error:
        #             print("Error in MTLR calculation:", error)
        #             pass
