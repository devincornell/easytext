

# Easy Text Analysis

Text analysis for those of us that don't want to code.

## Features

* topic modeling with LDA or NMF
* GloVe Word Embedding algorithm
* sentiment analysis
* named entity recognition
* prepositional phrase detector
* noun-verb detector

**Subcommands**
```
positional arguments:
  {topicmodel,glove,entities,grammar}
    topicmodel          Run topic modeling algorithms (LDA or NMF).
    glove               Run glove algorithm.
    entities            Run Named Entity Recognition (NER).
    grammar             Run grammatical expression extraction.

optional arguments:
  -h, --help            show this help message and exit

```


### Topic Modeling

From the docs:

```
usage: __main__.py topicmodel [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -n
                              NUMTOPICS [-t TYPE] [-s SEED] [-m MIN_TF]
                              [-nswm]
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

**Latent Dirichlet Allocation Example**
```
python -m easytext topicmodel example_tmp/*.txt topicmodel_lda.xlsx --numtopics 10 --min_tf 5 --nosave_wordmatrix
```


**Non-negative Matrix Factorization Example**
```
python -m easytext topicmodel example_tmp/*.txt topicmodel_lda.xlsx --type NMF --numtopics 10 --min_tf 5 -nswm
```


### GloVe Word Embedding

From the docs:
```
usage: __main__.py glove [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -d
                         DIMENSIONS [-kw KEYWORDS] [-s SEED] [-m MIN_TF]
                         [-nswm]
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
  -d DIMENSIONS, --dimensions DIMENSIONS
                        Numer of embedding dimensions.
  -kw KEYWORDS, --keywords KEYWORDS
                        Keywords orient embedding dimensions.
  -s SEED, --seed SEED  Integer to see glove model estimation.
  -m MIN_TF, --min_tf MIN_TF
                        Seed to be used to init topic model.
  -nswm, --nosave_wordmatrix
                        Don't save word matrix in excel (helps to make smaller
                        files).
```

**GloVe Example**

```
python -m easytext glove example_tmp/*.txt hi.xlsx -d 100 -m 5 -nswm
```

