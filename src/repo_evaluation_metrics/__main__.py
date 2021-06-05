#!/usr/bin/env python3
import argparse
import os
import sys
from src.get_programming_languages_precentage.get_precentage import run

parser = argparse.ArgumentParser(
    description="evaluation of usage of programming language"
)

parser.add_argument(
    "-dir", "--directory",
    dest="cloc_files",
    type=str,
    required=True,
    help="The directory of cloc csv files"
)

parser.add_argument(
    "-t", "--tool",
    dest="tool",
    type=str,
    required=True,
    help="The tool which is under evaluating"
)


def parse_args(cloc_directory, tool):
    try:
        assert isinstance(cloc_directory, str)
        assert cloc_directory.strip() != ""
        assert isinstance(tool, str)
        assert tool.strip() != ""
    except:
        parser.print_help()
        raise KeyError


def main():
    args = vars(parser.parse_args())
    try:
        parse_args(args["cloc_files"], args["tool"])
    except KeyError:
        sys.exit(0)
    sys.exit(run(args["cloc_files"], args["tool"]))
