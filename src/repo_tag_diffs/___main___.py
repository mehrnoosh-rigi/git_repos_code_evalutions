#!/usr/bin/env python3
import argparse
import os
import sys
from src.repo_tag_diffs.run_app import run

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

parser.add_argument(
    "-t", "--tool",
    dest="tool",
    type=str,
    required=True,
    help="The tool which is under evaluating"
)


def parse_args(json_directory, tool):
    try:
        assert isinstance(json_directory, str)
        assert json_directory.strip() != ""
        assert isinstance(tool, str)
        assert tool.strip() != ""
    except:
        parser.print_help()
        raise KeyError


def main():
    args = vars(parser.parse_args())
    try:
        parse_args(args["json-file-directory"], args["tool"])
    except KeyError:
        sys.exit(0)
    sys.exit(run(args["json-file-directory"], args["tool"]))
