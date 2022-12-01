import json
from src.gui.dashboard import dashboard


def append_to_result_file(key, value, file):

    """
    Append to the result file
    :param file: result file
    :param key: is the Key of object
    :param value: is the value of object
    """
    # repo_name = self.github_repo["name"]
    try:
        with open(file, "r+") as outfile:
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


def calculate_TLR(result_file, file_path):
    TTLs = [v for k, v in result_file.items() if k.startswith('TTL')]
    TTLs_number = len(TTLs)
    if TTLs_number == 0:
        append_to_result_file("Sum_TTL", 0, file_path)
        append_to_result_file("Average_TTL", 0, file_path)
    else:
        sum_TTL = 0
        for TTL in TTLs:
            sum_TTL = sum_TTL + TTL
        average_TTL = sum_TTL / TTLs_number
        append_to_result_file("Sum_TTL", sum_TTL, file_path)
        append_to_result_file("Average_TTL", average_TTL, file_path)
    print("------Done TTL------")


def calculate_TDiff(result_file, file_path):
    TDiffs = [v for k, v in result_file.items() if k.startswith('Tdiff')]
    TTLs_number = len(TDiffs)
    if TTLs_number == 0:
        append_to_result_file("Sum_TDiff", 0, file_path)
        append_to_result_file("AVG_TDiff", 0, file_path)

    else:
        sum_TDiff = 0
        for TDiff in TDiffs:
            sum_TDiff = sum_TDiff - TDiff
        average_TDiff = sum_TDiff / TTLs_number
        append_to_result_file("Sum_TDiff", sum_TDiff, file_path)
        append_to_result_file("AVG_TDiff", average_TDiff, file_path)
    print("------Done TDiff------")


def run():
    dashboard()
