import json

import PySimpleGUI as sg

from src.entities.repos import GitRepository


def dashboard():
    layout = [
        [sg.Input(), sg.FileBrowse("Select Result File", key="-IN-")],
        [sg.Button("Clone Repo"),
         sg.Button("Evaluate Repo"),
         # sg.Button("TLR"),
         sg.Button("Delete Repo"),
         sg.Cancel()],
    ]

    window = sg.Window("WEB APPLICATION SCRIPTED TESTS ANALYZES", layout, default_element_size=(150, 900))

    while True:
        event, values = window.read()
        if event is None or event == "Cancel" or event == sg.WIN_CLOSED:
            break

        try:
            file_path = values["-IN-"]
            tool = "selenium" if "selenium" in file_path else "cypress"
            with open(file_path) as f:
                repos = json.load(f)
                for repo in repos:
                    git_repository = GitRepository(repo, tool)
                    if event == "Clone Repo":
                        try:
                            from src.repo_evaluation_metrics.run_evaluation import clone_repo
                            clone_repo(git_repository=git_repository)
                        except OSError:
                            print("OS Error", OSError)
                    elif event == "Evaluate Repo":
                        try:
                            from src.repo_evaluation_metrics.run_evaluation import evaluate_repo
                            evaluate_repo(git_repository)
                        except NotImplementedError:
                            print("Not Implemented Error", NotImplementedError)
                    # elif event == "TLR":
                    #     try:
                    #         from src.repo_evaluation_metrics.run_evaluation import calculate_TLR
                    #         calculate_TLR(git_repository)
                    #     except NotImplementedError:
                    #         print("Not Implemented Error", NotImplementedError)
                    elif event == "Delete Repo":
                        try:
                            from src.repo_evaluation_metrics.run_evaluation import delete_repo
                            delete_repo(git_repository)
                        except OSError:
                            print("Deletion Error", OSError)
        except Exception as error:
            print("error>>>", error)


# TODO:
# Read selenium path files
# select file
# clone content of files
# extract data
# delete file
