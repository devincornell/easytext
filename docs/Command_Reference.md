# EasyText Command Line Guide

This guide covers the command line interface for the EasyText package. For the EasyText documentation overview, view the [README.md](/README.md) page. This interface allows users to issue a single command to read in text data as a spreadsheet column or list of text files, parse it using spacy, and output the result in another results spreadsheet. Almost all of the EasyText interface is available through these commands, and the interface is organized through a series of subcommands which are explained below.

For a broader overview of EasyText package functionality, see the main [README.md](/README.md).

Once installed, the easytext command line interface can be accessed through the system command "python -m easytext". To get details of the available commands, issue the help flag like this: "python -m easytext --help".

## Input/Output Parameters

All EasyText commands require an input of either text files or a spreadsheet, and output a single spreadsheet with the desired document information. The terminology for the base unit of analyses is the "document", but in reality you can consider paragraphs, sentences, or even lists of words to be EasyText documents. Each document also has a name associated with it, although the source of the names varies by the input type (explained below). The document names will appear for reference in the final output.

### Input Types

There are three data input types accepted: (1) single text files, where every line is a document and line numbers are document names; (2) multiple text files, where each filename is a document name and the text in each file are documents; and (3) spreadsheets (.csv, .xls, or .xlsx) where the document name and text data column names must be specified manually.

**Single Input Text File**: i.e. "myfolder/mydocs.txt"

If a single text file with the ".txt" extension is given (this extension _must_ be used - this is to prevent the accidental input of a binary file as input), each line of the text file will be considered as a separate document. Document names are the line numbers on which they appeared.

Example (using wordcount subcommand command as an example):

```
python -m easytext wordcount afolder/docdata.txt myfolder/myoutput.xlsx
```

**Multiple Input Text Files**: i.e. "myfolder/\*.txt"

In the case that multiple text files are input, the base filenames (i.e. all but file extension) will be used as the document names in the output spreadsheet.

Example (using wordcount subcommand command as an example):

```
python -m easytext wordcount afolder/*.txt myfolder/myoutput.xlsx
```


**Spreadsheet Input File**: i.e. "myspreadsheet.csv"

If using a spreadsheet input (.csv, .xls, or .xlsx), you will need to manually specify the column name in which document names appear (use the --doclabelcol argument) and the column name for the text data (use the --textcol). These files are opened using pandas, so the first line will be considered as column names.

Example (using wordcount subcommand command as an example):

```
python -m easytext wordcount mytextspreadsheet.csv myfolder/myoutput.xlsx --textcol "text" --doclabelcol "docname"
```

### Output Files


EasyText commands always output a single excel file, except in the case when the spreadsheet would be too large, in which case an hdf file is created with the extension ".h5" instead of ".xlsx". This is because there is a maximum file size on excel spreadsheets. Outputs are excel spreadsheets or hdf files because they often contain multiple "sheets" of data, or multiple tables within a single file.

The hdf output behavior can be supressed using the "-nhd" or "--nohdfonfail" flags with any command. Hdf files may be less preferred because they are more difficult to view with standard desktop software in comparison to spreadsheets. If a smaller output file is needed to produce a valid spreadsheet, commands usually have features which can allow users to extract only the most significant data in the resulting output file.

This example shows "myfolder/myoutput.xlsx" as the output file and will not ouput a .h5 file if the result is too big:

```
python -m easytext wordcount afolder/*.txt myfolder/myoutput.xlsx --nohdfonfail
```

### Human-Readable Formats

Many (but not all) commands also have a feature that changes the output to a human-readable format using `-hr` or `--human-readable`. While the machine-readable (default) mode has a good structure for further analysis using quantitative or computational methods, the human readable output is mostly a convenience tool for exploring your data.

In the example image below, I show a basic sentiment analysis output in which I do not use the human-readable format. Each row is a document, and there is one column for positive sentiment and a column for negative sentiment.

![Machine-Readable Sentiment Output](/figs/sentiment_machine.png)

In contrast, this is the output of the human-readable version. As one scans through each row, you can easily tell wether the document has more positive or negative sentiment because they are sorted. Whereas document `101607` and `102622` have more negative sentiment, `103110` has more positive sentiment.

![Human-Readable Sentiment Output](/figs/sentiment_human.png)


Not all commands have this option, so it may be best to go through the `--help` documentation to see which ones do.



## Sub-Command Documentation

The EasyText command line interface is organized into a series of subcommands. To see the subcommands listed, use the `python -m easytext --help` command. This is a list of the subcommands currently available from the EasyText interface:

* **wordcount**: Word count across corpus, either by (a) manually selecting words to count or (b) selecting a minimum frequency of words to count.
* **sentiment**: Compute sentiment analysis on corpus using Stanford empath.
* **entities**: Run Spacy Named Entity Recognition (NER).
* **topicmodel**: Run topic modeling algorithms (LDA or NMF).
* **glove**: Run glove algorithm.
* **grammar**: Grammatical relations: noun phrases, noun-verbs, entity-verbs, prepositional phrases}.

All subcommands essentially have the same arguments for infiles, outfile, -h for help, -dn for document label column (in case of spreadsheet input), -c for text column name (also in case of spreadsheet input), and -nhd to indicate that it should not output an .h5 file if the output is too large for an excel file (which is the default behavior, so-as to prevent processing time of large datasets). More detail is in the relevant parts of the documentation.

```
usage: __main__.py topicmodel [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -n
                              NUMTOPICS [-t TYPE] [-s SEED] [-m MIN_TF]
                              [-nswm]
                              infiles [infiles ...] outfile

positional arguments:
  infiles               Input files as either a single text file (must be
                        .txt), multiple text files (specify with glob (i.e.
                        myfolder/*.txt), or a spreadsheet (.csv, .xls, .xlsx)
                        with document name "--doclabel" and text data "--
                        textcol" column names.
  outfile               Output spreadsheet. Should end in .xls or .h5
                        depending on desired format. If command output is too
                        large to be an excel spreadsheet, will save to hdf
                        unless "--nohdfonfail" flag is used.

optional arguments:
  -h, --help            show this help message and exit
  -dn DOCLABELCOL, --doclabelcol DOCLABELCOL
                        Column name for document title/id.
  -c TEXTCOL, --textcol TEXTCOL
                        Column name of text data (if excel file provided).
  -nhd, --nohdfonfail   Don't write hdf if the data is too big for excel.

```

### Word Count Subcommand

This feature simply counts the frequency of word appearance in each document. By default, this command will count occurrence of all words in the corpus, but users can specify the lower frequency cutoff with the `-m` argument. Additionally, users can use the `-w` argument to specify words that should be counted in the corpus, instead of counting corpus words.

```
usage: __main__.py wordcount [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd]
                             [-w WORDS] [-m MIN_TF] [-hr]
                             infiles [infiles ...] outfile
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

The output file contains a single sheet where each document is a row and each column is an integer count of appearances (of course, different for human-readable mode).

### Sentiment Analysis Subcommand

This feature uses the [python package](https://github.com/Ejhfast/empath-client) of the [Stanford Empath lexicon](https://hci.stanford.edu/publications/2016/ethan/empath-chi-2016.pdf) for counting words that belong to each of a number of categories, one of which is sentiment.

```
usage: __main__.py sentiment [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] [-o]
                             [-n] [-hr]
                             infiles [infiles ...] outfile
optional arguments:
  -o, --posneg-only     Include only positive and negative emotion categories.
  -n, --no-normalize    Don't normalize counts by document length.
  -hr, --human-readable Organize output to be read by humans.
```

The output sheet 'report' organizes each row as a document and each column as a sentiment category. The 'summary' sheet shows a ranking of categories most associated with each document.




### Named Entity Recognition (NER) Subcommand

A common tool in text analysis is the ability to identify multi-word proper nouns in texts. Fortunately much of the groundwork for these analyses have been constructed. This command simply counts the number of times each identified named entity appears. Users can specify a minimum term frequency using the `--min_df` argument, or specify particular entity types using the `--use-types` argument (more details about entity type names can be found on the [Spacy NER Annotation Specification page](https://spacy.io/api/annotation#named-entities)). Similarly, one can specify types to ignore.

```
usage: __main__.py entities [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd]
                            [-m MIN_TF] [-hr] [-ut USE_TYPES]
                            [-it IGNORE_TYPES]
                            infiles [infiles ...] outfile

optional arguments:
  -m MIN_TF, --min_tf MIN_TF
                        Minimum number of total entity occurrences to include
                        in the model.
  -hr, --human-readable
                        Organize output to be read by humans.
  -ut USE_TYPES, --use-types USE_TYPES
                        Entity types to use. Format: "etype1,etype2".
  -it IGNORE_TYPES, --ignore-types IGNORE_TYPES
                        Entity types to ignore. Format: "etype1,etype2".
```

A basic list of entity types is given below. For full documentation, see the [Spacy NER Annotation Specification page](https://spacy.io/api/annotation#named-entities).

```
TYPE	DESCRIPTION
PERSON	People, including fictional.
NORP	Nationalities or religious or political groups.
FAC	Buildings, airports, highways, bridges, etc.
ORG	Companies, agencies, institutions, etc.
GPE	Countries, cities, states.
LOC	Non-GPE locations, mountain ranges, bodies of water.
PRODUCT	Objects, vehicles, foods, etc. (Not services.)
EVENT	Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART	Titles of books, songs, etc.
LAW	Named documents made into laws.
LANGUAGE	Any named language.
DATE	Absolute or relative dates or periods.
TIME	Times smaller than a day.
PERCENT	Percentage, including ”%“.
MONEY	Monetary values, including unit.
QUANTITY	Measurements, as of weight or distance.
ORDINAL	“first”, “second”, etc.
CARDINAL	Numerals that do not fall under another type.
```


### Topic Modeling Subcommand

The topic modeling subcommand allows one to run the LDA or NMF topic modeling algorithms on a corpus of documents. The default algorithm is LDA but one can also specify NMF using the `-t` argument, the number of topics using the `-n` argumnent, the algorithm seed using `-s` (for reproducability between runs), a frequency cutoff threshold using the `-m` command, and choose wether or not to save the word matrix using the `-nswm` flag. The word matrix can somtimes be huge, so omission might be desirable if an excel output is needed.

```
usage: __main__.py topicmodel [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -n
                              NUMTOPICS [-t TYPE] [-s SEED] [-m MIN_TF]
                              [-nswm]
                              infiles [infiles ...] outfile
optional arguments:
  -n NUMTOPICS, --numtopics NUMTOPICS
                        Numer of topics.
  -t TYPE, --type TYPE  From ('lda','nmf') choose algorithm.
  -s SEED, --seed SEED  Seed to be used to init topic model.
  -m MIN_TF, --min_tf MIN_TF
                        Seed to be used to init topic model.
  -nswm, --nosave_wordmatrix
                        Don't save word matrix in excel (helps to make smaller
                        files).
```


### GloVe Algorithm Subcommand

The glove algorithm subcommand allows the user to construct a glove model on the corpus, assigning vectors to both words and documents through (see details in the [`transform_paragraph` function of the python-glove package](https://github.com/maciejkula/glove-python/blob/master/glove/glove.py)). Users can specify the number of embedding dimensions, keywords around which to orient the embedding space (very experimental), and use the `-nswm` flag to omit the word vector data from the final spreadsheet (wich can always be gathered upon anothe run of the command).

```
usage: __main__.py glove [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -d
                         DIMENSIONS [-kw KEYWORDS] [-m MIN_TF] [-nswm]
                         infiles [infiles ...] outfile

optional arguments:
  -d DIMENSIONS, --dimensions DIMENSIONS
                        Numer of embedding dimensions.
  -kw KEYWORDS, --keywords KEYWORDS
                        Keywords orient embedding dimensions. Format:
                        "word1,word2|word3", where vector dimension 1 is
                        "word1" + "word2", and dimension 2 is the vector
                        "word3" rejected from dimension 1.
  -m MIN_TF, --min_tf MIN_TF
                        Minimum number of word occurrences to include in the
                        model.
  -nswm, --nosave_wordmatrix
                        Don't save word matrix in excel (helps to make smaller
                        files).

```


### Grammar Subcommand

The Grammar subcommand, unlike others, is also organized into a series of subcommands. The subcommands available can extract noun phrases (`nounphrases`), noun-verb pairs (`nounverbs`), entity-verb pairs (`entverbs`), and prepositional phrases (`prepositions`) from the text documents. These are the available subcommands:

* nounphrases         Extract noun phrases.
* nounverbs           Extract noun-verb pairs.
* entverbs            Extract entity-verb pairs.
* prepositions        Extract prepositional phrases.

All of the grammar sub-sub-commands take the same two arguments. `-m` sets a lower limit on frequencies of phrases and `-hr` specifies human-readable output.

```
  -m MIN_TF, --min_tf MIN_TF
                        Min phrase count to include.
  -hr, --human-readable
                        Produce human readable output.
```

#### Noun Phrase Sub-sub-command

This subcommand will identify noun phrases in the documents.


#### Noun-Verb Sub-sub-command

This subcommand will identify noun-verb pairs in the documents.


#### Entity-Verb Sub-sub-command

This subcommand will identify entity-verb relations in the documents.


#### Prepositional Phrase Sub-sub-command

This subcommand will identify prepositional phrases in the documents.


