# EasyText Command Line Guide

This guide covers the command line interface for the EasyText package. This interface allows users to issue a single command to read in text data as a spreadsheet column or list of text files, parse it using spacy, and output the result in another results spreadsheet. Almost all of the EasyText interface is available through these commands, and the interface is organized through a series of subcommands which are explained below.

For a broader overview of EasyText package functionality, see the main [README.md](https://github.com/devincornell/easytext/blob/master/README.md).

Once installed, the easytext command line interface can be accessed through the system command "python -m easytext". To get details of the available commands, issue the help flag like this: "python -m easytext --help".

## Input/Output Parameters

All EasyText commands require an input of either text files or a spreadsheet, and output a single spreadsheet with the desired document information. The terminology for the base unit of analyses is the "document", but in reality you can consider paragraphs, sentences, or even lists of words to be EasyText documents. Each document also has a name associated with it, although the source of the names varies by the input type (explained below). The document names will appear for reference in the final output.

### Input Types

There are three data input types accepted: (1) single text files, where every line is a document and line numbers are document names; (2) multiple text files, where each filename is a document name and the text in each file are documents; and (3) spreadsheets (.csv, .xls, or .xlsx) where the document name and text data column names must be specified manually.

**Single Text File**: i.e. "myfolder/mydocs.txt"

If a single text file with the ".txt" extension is given (this extension _must_ be used - this is to prevent the accidental input of a binary file as input), each line of the text file will be considered as a separate document. Document names are the line numbers on which they appeared.

**Multiple Text Files**: i.e. "myfolder/\*.txt"

In the case that multiple text files are input, the base filenames (i.e. all but file extension) will be used as the document names in the output spreadsheet.

**Spreadsheet File**: i.e. "myspreadsheet.csv"

If using a spreadsheet input (.csv, .xls, or .xlsx), you will need to manually specify the column name in which document names appear (use the --doclabelcol argument) and the column name for the text data (use the --textcol). These files are opened using pandas, so the first line will be considered as column names.


### Output Files


EasyText commands always output a single excel file, except in the case when the spreadsheet would be too large, in which case an hdf file is created with the extension ".h5" instead of ".xlsx". This is because there is a maximum file size on excel spreadsheets. Outputs are excel spreadsheets or hdf files because they often contain multiple "sheets" of data, or multiple tables within a single file.

The hdf output behavior can be supressed using the -nhd or --nohdfonfail flags on any command. Hdf files may be less preferred because they are more difficult to view with standard desktop software in comparison to spreadsheets. If a smaller output file is needed to produce a valid spreadsheet, commands usually have features which can allow users to extract only the most significant data in the resulting output file.



positional arguments:
  infiles               Input files.
  outfile               Output file.

optional arguments:
  -h, --help            show this help message and exit
  -dn DOCLABELCOL, --doclabelcol DOCLABELCOL
                        Column name for document title/id.
  -c TEXTCOL, --textcol TEXTCOL
                        Column name of text data (if excel file provided).
  -nhd, --nohdfonfail   Don't write hdf if the data is too big for excel.



## Command Overview

```

python -m easytext --help
usage: __main__.py [-h]
                   {wordcount,sentiment,entities,topicmodel,glove,grammar} ...

positional arguments:
  {wordcount,sentiment,entities,topicmodel,glove,grammar}
    wordcount           Word count across corpus, either by (a) manually
                        selecting words to count or (b) selecting a minimum
                        frequency of words to count.
    sentiment           Compute sentiment analysis on corpus using Stanford
                        empath.
    entities            Run Spacy Named Entity Recognition (NER).
    topicmodel          Run topic modeling algorithms (LDA or NMF).
    glove               Run glove algorithm.
    grammar             Grammatical relations: noun phrases, noun-verbs,
                        entity-verbs, prepositional phrases}.

optional arguments:
  -h, --help            show this help message and exit


```

## Word Counts

One of the most basic features of the command line interface is the ability to simply count the number of times each word appears in each document. This feature works by either specifying the words that you wish to count or by specifying a minimum number of occurrences in which a word needs to be used to be included.

```

usage: __main__.py wordcount [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd]
                             [-w WORDS] [-m MIN_TF] [-hr]
                             infiles [infiles ...] outfile

positional arguments:
  infiles               Input files.
  outfile               Output file.

optional arguments:
  -h, --help            show this help message and exit
  -dn DOCLABELCOL, --doclabelcol DOCLABELCOL
                        Column name for document title/id.
  -c TEXTCOL, --textcol TEXTCOL
                        Column name of text data (if excel file provided).
  -nhd, --nohdfonfail   Don't write hdf if the data is too big for excel.
  -w WORDS, --words WORDS
                        Comma-separated words to count in each document. Each
                        word will be a column. i.e. "word1,word2" to count
                        just two words.
  -m MIN_TF, --min_tf MIN_TF
                        Count all words that appear a minimum of min_tf times
                        in corpus. Warning: could lead to really large &
                        sparse output files.
  -hr, --human-readable
                        Organize output to be read by humans.

```


