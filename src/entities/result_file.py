import json
from threading import Lock


class ResultFile:
    file_lock = Lock()

    def __init__(self, repo_name, tool):
        self.repo_name = repo_name
        self.tool = tool

    def create_result_file(self):
        try:
            with type(self).file_lock:
                with open(f"results/repos_statistics/{self.tool}/{self.repo_name}.json", "w") as outfile:
                    data = {'repo_name': self.repo_name}
                    json.dump(data, outfile)
                    outfile.close()
        except Exception as e:
            print("Error in creation of result file", e)

    def append_to_result_file(self, key, value):
        """
        Append to the result file
        :param key: is the Key of object
        :param value: is the value of object
        """
        # repo_name = self.github_repo["name"]
        try:
            with type(self).file_lock:
                with open(f"../../repos_statistics/{self.tool}/{self.repo_name}.json", "r+") as outfile:
                    # First we load existing data into a dict.
                    file_data = json.load(outfile)
                    # Join new_data with file_data inside emp_details
                    if key not in file_data:
                        file_data[key] = value
                        # Sets file's current position at offset.
                        outfile.seek(0)
                        # convert back to json.
                        json.dump(file_data, outfile, indent=4)
                    outfile.close()
        except Exception as e:
            print("Error in appending to the result file", e, key, value)

    def read_result_file(self):
        try:
            with type(self).file_lock:
                with open(f"../../repos_statistics/{self.tool}/{self.repo_name}.json", "r") as result_file:
                    data = json.load(result_file)
                    result_file.close()
                    return data
        except Exception as e:
            print("Error in reading result file", e)
