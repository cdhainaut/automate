import argparse
from math import e
import os
from os import path
import pandas as pd
from automate.utils import query_yes_no


class Filterer:
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

    def build_args(self):
        self.parser.add_argument(
            "input", nargs="+", help=".csv files to be used"
        )
        self.parser.add_argument(
            "-c",
            "--columns",
            nargs="?",
            help="Columns to keep in csv",
            default="columns_to_filter",
        )

    @staticmethod
    def do_actions(args):

        path_execution = os.getcwd()
        path_filtered = os.path.join(path_execution, "filtered_res")

        if not os.path.isdir(path_filtered):
            os.makedirs(path_filtered)
        existing_files = [
            os.path.basename(i)
            for i in args.input
            if os.path.basename(i) in os.listdir(path_filtered)
        ]
        if len(existing_files) > 0:
            process_existing = query_yes_no(
                "{} already exist. Process them anyway ?".format(existing_files)
            )

        for i in args.input:
            process = True
            filename = os.path.basename(i)
            if filename in existing_files:
                process = process_existing
            if process:
                if not args.columns == "all":
                    with open(args.columns.rstrip(), "r") as f:
                        columns = [
                            line.rstrip()
                            for line in f.readlines()
                            if line.rstrip() != ""
                        ]
                else:
                    columns = None

                try:
                    df = pd.read_csv(i, usecols=columns)

                    export_path = os.path.join(path_filtered, filename)
                    print("> Export to " + export_path)

                    df.to_csv(export_path, index=False)
                except Exception as e:
                    print("> ! Impossible to process " + str(i))
                    print(e)


def cli_func():
    parser = argparse.ArgumentParser(
        description="This script manipulates a dataframe from Gomboc"
    )
    parser.add_argument("input", nargs="+", help=".csv files to be used")
    parser.add_argument(
        "-c",
        "--columns",
        nargs="?",
        help="Columns to keep in csv",
        default="columns_to_filter",
    )
    return parser


if __name__ == "__main__":
    args = cli_func().parse_args()

    path_execution = os.getcwd()
    path_filtered = os.path.join(path_execution, "filtered_res")

    if not os.path.isdir(path_filtered):
        os.makedirs(path_filtered)
    existing_files = [
        os.path.basename(i)
        for i in args.input
        if os.path.basename(i) in os.listdir(path_filtered)
    ]
    if len(existing_files) > 0:
        process_existing = query_yes_no(
            "{} already exist. Process them anyway ?".format(existing_files)
        )

    for i in args.input:
        process = True
        filename = os.path.basename(i)
        if filename in existing_files:
            process = process_existing
        if process:
            if not args.columns == "all":
                with open(args.columns.rstrip(), "r") as f:
                    columns = [
                        line.rstrip()
                        for line in f.readlines()
                        if line.rstrip() != ""
                    ]
            else:
                columns = None

            try:
                df = pd.read_csv(i, usecols=columns)

                export_path = os.path.join(path_filtered, filename)
                print("> Export to " + export_path)

                df.to_csv(export_path, index=False)
            except Exception as e:
                print("> ! Impossible to process " + str(i))
                print(e)
