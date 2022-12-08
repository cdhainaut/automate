import argparse
import datetime
import os
from os import path
import pandas as pd
import numpy as np
from ..utils.utils import query_yes_no


def dateparse(time_in_secs):
    return datetime.datetime.fromtimestamp(float(time_in_secs))


columns_to_keep = ["Time"]


class Resampler:
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

    def build_args(self):

        self.parser.add_argument(
            "input", nargs="+", help=".csv files to be used"
        )
        self.parser.add_argument(
            "-dt",
            "--timestep",
            nargs="?",
            help="Timestep to use for data sample",
            default="0.2S",
        )
        self.parser.add_argument(
            "-id",
            "--index",
            nargs="?",
            type=str,
            help="Index column to be used for resampling",
            default="Time",
        )

    @staticmethod
    def do_actions(args):
        path_execution = os.getcwd()
        path_resample = os.path.join(path_execution, "data_" + args.timestep)
        if not os.path.isdir(path_resample):
            os.makedirs(path_resample)
        existing_files = [
            os.path.basename(i)
            for i in args.input
            if os.path.basename(i) in os.listdir(path_resample)
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

                df = (
                    pd.read_csv(
                        i,
                        index_col=args.index,
                        parse_dates=True,
                        date_parser=dateparse,
                    )
                    .resample(args.timestep)
                    .interpolate()
                    .reset_index()
                )
                df.replace(-np.inf, np.nan, inplace=True)
                df.replace(np.inf, np.nan, inplace=True)
                df.ffill(inplace=True)

                export_path = os.path.join(path_resample, filename)
                print("> Export to " + export_path)

                df.to_csv(export_path, index=False)


def cli_func():
    parser = argparse.ArgumentParser(
        description="This script manipulates a dataframe from Gomboc"
    )
    parser.add_argument("input", nargs="+", help=".csv files to be used")
    parser.add_argument(
        "-dt",
        "--timestep",
        nargs="?",
        help="Timestep to use for data sample",
        default="0.2S",
    )
    return parser


if __name__ == "__main__":
    args = cli_func().parse_args()
    path_execution = os.getcwd()
    path_resample = os.path.join(path_execution, "data_" + args.timestep)
    if not os.path.isdir(path_resample):
        os.makedirs(path_resample)
    existing_files = [
        os.path.basename(i)
        for i in args.input
        if os.path.basename(i) in os.listdir(path_resample)
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

            df = (
                pd.read_csv(
                    i, index_col="Time", parse_dates=True, date_parser=dateparse
                )
                .resample(args.timestep)
                .interpolate()
                .reset_index()
            )

            df.replace(-np.inf, np.nan, inplace=True)
            df.replace(np.inf, np.nan, inplace=True)
            df.ffill(inplace=True)

            export_path = os.path.join(path_resample, filename)
            print("> Export to " + export_path)

            df.to_csv(export_path, index=False)
