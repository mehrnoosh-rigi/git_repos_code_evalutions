import logging
import os
import csv
import git


class GitRepository:
    def __init__(self, github_repo, tool):
        self.github_repo = github_repo
        self.tool = tool
        self.project_root = f"results/cloned_programs/{github_repo['name']}"
        self.tags = []

    def clone_repo(self):
        try:
            # git.Git("results/cloned_programs").clone("https://github.com/GoogleChrome/workbox.git")
            git.Git("results/cloned_programs").clone(self.github_repo["clone_url"])
            print("clone", self.github_repo["clone_url"])

        except Exception as e:
            logging.info("cloning error:", e)

    def list_tags(self):
        try:
            # self.tags = git.Repo(f"results/cloned_programs/workbox").tags
            self.tags = git.Repo(self.project_root).tags
        except Exception as e:
            logging.info("list tags error", e)

    def get_lines_of_code(self):
        try:
            os.chdir("./results/cloned_programs")
            # cloc = os.system(f"cloc {self.github_repo['name']}")
            git_name = self.github_repo['name']
            os.system(f"cloc {self.github_repo['name']} --csv --out=../csv/{self.tool}/{git_name}/cloc/{self.github_repo['name']}")
            os.chdir("..")
            # print("current dir", os.getcwd())
            # with open(f"csv/self.github_repo['name']", "w", newline="") as csvfile:
            # with open("csv/workbox", 'w', newline='\n') as csvfile:
            #     loc = csv.writer(csvfile, delimiter=' ',
            #                      quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            #     loc.writerow("TOTAL LOC")
            #     loc.writerow(cloc)

        except Exception as e:
            logging.info("cloc lines of code", e)

    def tags_diff(self):
        try:
            for i in range(len(self.tags) - 1):
                os.chdir(f"./results/cloned_programs/{self.github_repo['name']}")
                # print("current dir", os.getcwd())
                git_name = self.github_repo['name']
                os.system(f"cloc --git --diff {self.tags[i]} {self.tags[i+1]} --csv --out=../../csv/{self.tool}/{git_name}/{self.tags[i]}_{self.tags[i+1]}")
                os.chdir("../..")

        except Exception as e:
            logging.info("tags different", e)

    def delete_repo(self):
        os.chdir("./results/cloned_programs")
        os.system(f"rm -rf {self.github_repo['name']}")
        os.chdir("..")
