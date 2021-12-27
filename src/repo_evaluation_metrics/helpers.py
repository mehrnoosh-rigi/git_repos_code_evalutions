import os
import subprocess


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
    return ".json" not in decoded_line and ".md" not in decoded_line \
           and ".npmignore" not in decoded_line \
           and ".gitignore" not in decoded_line \
           and ".yml" not in decoded_line

