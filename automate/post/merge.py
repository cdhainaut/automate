import pandas as pd
import os
import argparse
import numpy as np


parser = argparse.ArgumentParser(description='This script manipulates a dataframe from Gomboc')
parser.add_argument("-l","--left", nargs='+',	help=".csv files to be used")
parser.add_argument("-r","--right", nargs='+',	help=".csv files to be used")
args = parser.parse_args()

path_execution = os.getcwd()
path_merge = os.path.join(path_execution,"merged_res")


if not os.path.isdir(path_merge):
    os.makedirs(path_merge)

for l,r in zip(args.left,args.right):
    filename = os.path.basename(l)
    df = pd.merge(pd.read_csv(l),pd.read_csv(r))
    export_path = os.path.join(path_merge,filename)
    print("> Export to "+export_path)
    df.to_csv(export_path,index=False)
