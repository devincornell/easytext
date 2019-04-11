# Contributing to EasyText

This doc gives a brief description of how to make changes to both the API interface `easyparse()` and the command line interface.

## `easyparse()` API Interface Changes

There are three changes that need to be made when adding new functionality to the easytext command. It is relatively simple because the design is built on [Spacy pipeline components](https://spacy.io/usage/processing-pipelines). 

1. Create a new pipeline class in `pipelines.py` with `__init__` and `__call__` functions.

2. Register the compnent in the `ALL_COMPONENTS` with both spacy and EasyText dependencies.

## Command Line Interface

The process of updating a command require more steps. These steps cover how to add a new subcommand to the interface. Upon examining the `__main__.py` file, you can see that the subcommands are managed in a dictionary variable called `all_subcommands`, and the functions passed there are all defined in the file `subcommand_functions.py`.

To create a new subcommand called `mycommand`, for instance, simply follow these steps:

1. Create a function definition for `mycommand_args(main_parser, main_subparsers)`. This function will take in a parser and subparser [argparse objects](https://docs.python.org/3/library/argparse.html) and you will need to add the subcommand (`main_subparsers.add_parser()`) and any arguments your subcommand should take. This example below shos a single flag argument, `--do-something` which could activate some feature of your command, assuming you program it to do so.

```
def mycommand_args(main_parser, main_subparsers):
    newp = main_subparsers.add_parser('mycommand', help='My new command.')
    common_args(newp) # this will add args for input/output/nohdfonfail that apply to every function
    newp.add_argument('-d','--do-something', action='store_true', help='Flag to initiate some feature.')

```

2. Create a function definition for `subcommand_mycommand(texts, docnames, args)` that takes a list of texts, a list of docnames, and the argparse object. This code should be the body of your subcommand, and should return the name of the saved output file upon completion.

3. Register your functions as a new entry in the `all_subcommands` dictionary in `__main__.py`. The entry should look like this for our example:

```
'mycommand':{'argparser':mycommand_args, 'command':subcommand_mycommand},
```

That concludes the adding command line subcommands.

