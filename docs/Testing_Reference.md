
# Testing Reference

This is a short guide to testing EasyText when making changes. As the package includes both a python API and command line interface, there are to testing components.


## Example Data

The primary example data used in this package is the [sklearn newsgroup20](https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html). The code to access that dataset can be found in `example_data.py`. You can use the `get_testdata` function to get the data directly, or one of the other functions to save data directly to a single text file, multiple text files, or a spreadsheet with text data.


## API Interface Testing

The API interface tests are not particularly well-developed, but at least the code found in README.md can be found in the script `example_README.py`. This script extracts data from the sklearn and places it in lists of document strings and document names.


## Command Interface Testing

The command interface can be tested in the `example_commands.py` script. The script reads in a list of shell commands (currently `example_commands.sh` and `example_commands_spreadsheet.sh`) and runs all the commands there. Those shell scripts usually start by creating a temporary directory for output, and running the command `python example_data.py textfiles 100` (or `python example_data.py spreadsheet 100`) to create test data, either spreadsheets or individual text files. In those examples, the script will store 100 random documents from the newsgroup20 dataset in sklearn.

When running `example_commands.py`, the easiest way to identify a failure is by redirecting stdout but not stderr. Using the command below will store all the regular output in `TMP_DELETEME.txt` while printing the stderr onto your screen. That may be the easiest way to look for errors.

```
python example_commands.py > TMP_DELETEME.txt
```


