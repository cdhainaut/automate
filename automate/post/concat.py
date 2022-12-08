import pandas as pd
import os
import argparse
import numpy as np

def arcommand(func):
    return func
class Concatenator:
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

    def build_args(self):

        self.parser.add_argument("input", nargs="+", help=".csv files to be used")
        self.parser.add_argument(
            "-m",
            "--matrix",
            nargs="?",
            help=".csv Matrix to be used for results mapping",
            default=None,
        )
        self.parser.add_argument(
            "-j", "--join", nargs="?", help="Join method", default="outer"
        )
        self.parser.add_argument(
            "-s",
            "--skiprows",
            nargs="?",
            type=int,
            help="Number of top rows to skip",
        )
        self.parser.add_argument(
            "-w",
            "--windows",
            nargs=1,
            type=str2bool,
            help="Tell if .csv should be read as windows format",
            default=False,
        )
        self.parser.add_argument(
            "-mi", "--mapindex", nargs="?", type=str2bool, default=True
        )
        self.parser.add_argument(
            "-r",
            "--rename",
            nargs="+",
            type=str,
            default=["", ""],
            help="Column to rename to be used as following: -r old_name new_name",
        )
        self.parser.add_argument("-i", "--index", nargs="?", type=str, default="ID")
        self.parser.add_argument(
            "-n",
            "--name",
            nargs="?",
            type=str,
            default="file",
            help="Naming method. 'file' or 'dir'",
        )
        self.parser.add_argument(
            "-o", "--output", nargs="?", type=str, default="results_full.csv"
        
        )
    @staticmethod
    def do_actions(args):
        kwargs_read = {}
        if args.windows:
            kwargs_read = {"sep": ";", "decimal": ","}
        kwargs_concat = {}

        if args.mapindex:
            if args.name == "file":
                keys = [
                    os.path.splitext(os.path.basename(f))[0] for f in args.input
                ]
            else:
                keys = [os.path.dirname(f).split("/")[-1] for f in args.input]

            kwargs_concat = {"keys": keys, "names": [args.index]}

        df = pd.concat(
            [
                pd.read_csv(i, skiprows=args.skiprows, **kwargs_read).rename(
                    columns={args.rename[0]: args.rename[1]}
                )
                for i in args.input
            ],
            join=args.join,
            **kwargs_concat
        ).reset_index()

        if args.matrix is not None:
            matrix = pd.read_csv(args.matrix, **kwargs_read)
            df[args.index] = df[args.index].astype(matrix[args.index].dtype)
            df = df.merge(matrix, on=[args.index])

        df.to_csv(args.output, index=False)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")

def cli_func():
    parser = argparse.ArgumentParser(
        description="Concatenates dataframes together, using pandas.concat function. Check pandas documentation for more detailed usage"
    )
    parser.add_argument("input", nargs="+", help=".csv files to be used")
    parser.add_argument(
        "-m",
        "--matrix",
        nargs="?",
        help=".csv Matrix to be used for results mapping",
        default=None,
    )
    parser.add_argument(
        "-j", "--join", nargs="?", help="Join method", default="outer"
    )
    parser.add_argument(
        "-s",
        "--skiprows",
        nargs="?",
        type=int,
        help="Number of top rows to skip",
    )
    parser.add_argument(
        "-w",
        "--windows",
        nargs=1,
        type=str2bool,
        help="Tell if .csv should be read as windows format",
        default=False,
    )
    parser.add_argument(
        "-mi", "--mapindex", nargs="?", type=str2bool, default=True
    )
    parser.add_argument(
        "-r",
        "--rename",
        nargs="+",
        type=str,
        default=["", ""],
        help="Column to rename to be used as following: -r old_name new_name",
    )
    parser.add_argument("-i", "--index", nargs="?", type=str, default="ID")
    parser.add_argument(
        "-n",
        "--name",
        nargs="?",
        type=str,
        default="file",
        help="Naming method. 'file' or 'dir'",
    )
    parser.add_argument(
        "-o", "--output", nargs="?", type=str, default="results_full.csv"
    )
    return parser


if __name__ == "__main__":
    args = cli_func().parse_args()

    kwargs_read = {}
    if args.windows:
        kwargs_read = {"sep": ";", "decimal": ","}
    kwargs_concat = {}

    if args.mapindex:
        if args.name == "file":
            keys = [
                os.path.splitext(os.path.basename(f))[0] for f in args.input
            ]
        else:
            keys = [os.path.dirname(f).split("/")[-1] for f in args.input]

        kwargs_concat = {"keys": keys, "names": [args.index]}

    df = pd.concat(
        [
            pd.read_csv(i, skiprows=args.skiprows, **kwargs_read).rename(
                columns={args.rename[0]: args.rename[1]}
            )
            for i in args.input
        ],
        join=args.join,
        **kwargs_concat
    ).reset_index()

    if args.matrix is not None:
        matrix = pd.read_csv(args.matrix, **kwargs_read)
        df[args.index] = df[args.index].astype(matrix[args.index].dtype)
        df = df.merge(matrix, on=[args.index])
    print(df)

    df.to_csv(args.output, index=False)
