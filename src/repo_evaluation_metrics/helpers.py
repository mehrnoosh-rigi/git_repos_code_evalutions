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
           and ".yml" not in decoded_line \
           and ".txt" not in decoded_line \
           and "LICENSE" not in decoded_line \
           and ".conf" not in decoded_line \
           and ".png" not in decoded_line \
           and "css" not in decoded_line \
           and ".njk" not in decoded_line \
           and ".eslintrc" not in decoded_line \
           and ".d" not in decoded_line \
           and "/img" not in decoded_line \
           and "index" not in decoded_line \
           and ".pack" not in decoded_line \
           and ".idx" not in decoded_line \
           and "utils" not in decoded_line \





