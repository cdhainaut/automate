<div align="center">
  <img src="logo.png"><br>
</div>

# automate: Fast command line interface for automated data processing

automate is a command-line interface toolbox allowing to:
- Do fast data treatment (pre/post processing)
- Parse template files based on .csv matrices

This software essentially consists in using functions from Pandas (https://pandas.pydata.org/) library in command line.


## Prerequisistes
- python libraries: `pandas`,`numpy`

## Usage
Scripts can be used separately, but they also can be used in chain inside a bash script. For instance, the following script allows to treat .csv files from Gomboc saved inside /results folder:

```bash
automate filter results/* # Removes headers you don't need
automate average filtered_res/* # Returns an averaged dataframe and save them inside average_res/
automate concat average_res/* --matrix matrix.csv
```