import pandas as pd
import os
import argparse
import numpy as np
import datetime

def dateparse (time_in_secs):    
	return datetime.datetime.fromtimestamp(float(time_in_secs))

def cli_func():
    parser = argparse.ArgumentParser(description='Averages a single or multiple dataframes')
    parser.add_argument("input", nargs='+',	help=".csv files to be used")
    parser.add_argument("-w","--window",nargs='+',type=str,help="Time window cutoff",default=[float("-inf"),float("inf")])
    parser.add_argument("-c","--columns",nargs="*",help="Columns to average",default=["all"])
    parser.add_argument("-e","--exclude",nargs="*",help="Columns to exclude from average",default=["Time"])
    parser.add_argument("-t","--time",nargs="?",help="Time column name",default="Time")
    parser.add_argument('-on','--output_names', nargs='?',type=str, help='Output naming method. Can be "file" or "dir"',default='file')
    parser.add_argument('-od','--output_dir', nargs='?',type=str, help='Output directory. Options are "group", "current", or "each"',default='')
    return parser

if __name__ == '__main__':
    args = cli_func().parse_args()

    path_execution = os.getcwd()
    path_averages = os.path.join(path_execution,"average_res")

    if not os.path.isdir(path_averages):
        os.makedirs(path_averages)

    for i in args.input:
        print("> Opening "+i)
        df = pd.read_csv(i)
        time_mask = ((df[args.time] >= float(args.window[0])) & (df[args.time] <= float(args.window[1])))
        df = df[time_mask]


        df.replace(-np.inf,np.nan,inplace=True)
        df.replace(np.inf,np.nan,inplace=True)
        df.ffill(inplace=True)
        

        if args.columns[0] == "all":
            columns = df.columns
            print("> Calculate min, max, mean, std for all header")
        else:
            columns = args.columns
            print("> Calculate min, max, mean, std for :\n- "+"\n- ".join(args.columns))
        
        columns = filter(lambda x: x not in args.exclude, columns)
        for header in columns:
        
            df[header+"_min"] = np.min(df[header])
            df[header+"_max"] = np.max(df[header])
            df[header+"_mu"] = np.mean(df[header])
            df[header+"_sigma"] = np.std(df[header])
        filename = os.path.basename(i)

    
    
        df = df.tail(n=1)

        export_path = os.path.join(path_averages,filename)
        df.to_csv(export_path,index=False)
        print("> "+export_path+" successfully saved")