#!/usr/bin/env python3
import argparse
import sys
from src.code_evaluation_metrics.run_app import run

parser = argparse.ArgumentParser(
    description="Repositories metrics evaluator"
)

parser.add_argument(
    "-dir", "--directory",
    dest="json-file-directory",
    type=str,
    required=True,
    help="The directory of filtered json file that contains repositories information"
)


def parse_args(json_directory):
    try:
        assert isinstance(json_directory, str)
        assert json_directory.strip() != ""
    except:
        parser.print_help()
        raise KeyError


def main():
    args = vars(parser.parse_args())
    try:
        parse_args(args["json-file-directory"])
    except KeyError:
        sys.exit(0)
    sys.exit(run(args["json-file-directory"]))
