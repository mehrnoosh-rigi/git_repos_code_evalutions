import json

import PySimpleGUI as sg

from src.entities.repos import GitRepository


def dashboard():
    layout = [
        [sg.Input(), sg.FileBrowse("Select Result File", key="-IN-")],
        [sg.Button("TTL"),
         sg.Button("TLR"),
         sg.Button("TDiff"),
         sg.Button("MTLR"),
         sg.Cancel()],
    ]

    window = sg.Window("WEB APPLICATION SCRIPTED TESTS ANALYZES", layout, default_element_size=(150, 900))

    while True:
        event, values = window.read()
        if event is None or event == "Cancel" or event == sg.WIN_CLOSED:
            break

        try:
            file_path = values["-IN-"]
            with open(file_path, "r") as result_file:
                data = json.load(result_file)
                result_file.close()
                if event == "TTL":
                    try:
                        from src.repo_extract_conclusion.run_conclusion import calculate_TTL
                        calculate_TTL(data, file_path)
                    except OSError:
                        print("OS Error", OSError)
                elif event == "TDiff":
                    try:
                        from src.repo_extract_conclusion.run_conclusion import calculate_TDiff
                        calculate_TDiff(data, file_path)
                    except OSError:
                        print("OS Error", OSError)
                elif event == "TLR":
                    try:
                        from src.repo_extract_conclusion.run_conclusion import calculate_TLR
                        calculate_TLR(data, file_path)
                    except NotImplementedError:
                        print("Not Implemented Error", NotImplementedError)
                elif event == "MTLR":
                    try:
                        from src.repo_extract_conclusion.run_conclusion import calculate_MTLR
                        calculate_MTLR(data, file_path)
                    except NotImplementedError:
                        print("Not Implemented Error", NotImplementedError)
        except Exception as error:
            print("error>>>", error)

