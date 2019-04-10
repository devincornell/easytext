
# EasyText

This package combines several common text analysis algorithms into a single interface. It includes a simple interface for parsing text data through an API driven by custom Spacy pipeline components and an extensive command-line interface which wraps the EasyText api and other features. This document will cover primarily the Python API; for command line reference, see the documentation on the [Command Reference Page](/Command_Reference.md)).

The easytext interface can be divided into two sections: pre-processing with the `easyparse()` function and algorithm wrapper functions.

## Preprocessing Using `easyparse()` Function

The preprocessing features of EasyText can be accessed through the `easyparse()` function, which is primarily a wrapper around the `spacy.pipe()` method with custom pipeline components that accomplish common tasks. As a preliminary example, the basic workflow is to (1) acquire the texts as a list of strings (`texts` variable in this example), (2) choose the easyparse features you would like to enable, (3) call the `easyparse()` function in a loop, and (4) consume the resulting data. The following example shows a simple example using the 'wordlist' and 'entlist' features of EasyText.

```
from easytext import easyparse

texts # list of strings containing the texts of interest

components = ['wordlist', 'entlist']
nlp = spacy.load('en')
for etdoc in easyparse(nlp, texts, enable=components):
  print(etdoc['wordlist']) # prints list of tokens in the doc
  print(etdoc['entlist']) # prints list of Named Entities in the doc
```

### Preprocessing Feature List

The full list of preprocessing components is provided below. Each component has an associated output variable of the same name that will be contained in the document object output from the `easyparse()` function.

* **wordlist**: Extracts a list of tokens, including words and punctuation, that appear in the document.
* **sentlist**: Contains a list of sentence token lists that appear in the document.
* **entlist**: Contains a list of named entities observed in the document. Named entities are combined if they have the same representation after changing to lower case and removing whitespace.
* **prepphrases**: List of prepositional phrases found in the document.
* **nounverbs**: List of (noun, verb) pair tuples found in the document.
* **entverbs**: List of (entity, verb) pair tuples found in the document.
* **nounphrases**: List of nouns and noun phrases found in the document.

## Features


* word counts (using spacy library tokenizer)
* sentiment analysis (using python empath library)
* topic modeling with LDA or NMF (using sklearn library)
* GloVe Word Embedding algorithm (using python-glove package)
* named entity recognition (using spacy library ner)
* prepositional phrase detector (using spacy library parse trees)
* noun-verb detector (using spacy library parse trees)

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

### Word Counts

Will count the number of times words appear in the corpus, either by identifying terms that appear more than N times or by hand-selecting the words to count.

Uses spacy tokenizer.

#### Word Count Docs

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


#### Word Count Examples
```
python -m easytext wordcount tmp/*.txt testoutput/words_m10.xlsx --min_tf 10
```
Count every word that appears more than 10 times in the corpus.


```
python -m easytext wordcount tmp/*.txt testoutput/words_manual.xlsx --words 'news'
```
Count the number of times "news" appears in the corpus.

### Sentiment Analysis

Uses the Empath dictionary-based python library for calculating sentiment. Can choose to identify positive/negative sentiment only.

https://github.com/Ejhfast/empath-client


#### Sentiment Help Docs

```
usage: __main__.py sentiment [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] [-o]
                             [-n] [-hr]
                             infiles [infiles ...] outfile

  -o, --posneg-only     Include only positive and negative emotion categories.
  -n, --no-normalize    Don't normalize counts by document length.
  -hr, --human-readable
                        Organize output to be read by humans.
```


#### Sentiment Examples
```
python -m easytext sentiment tmp/*.txt testoutput/sent_vanilla.xlsx
```
Run full Empath sentiment analysis on corpus.

```
python -m easytext sentiment tmp/*.txt testoutput/sent_human.xlsx --human-readable
```
Make human-readable sentiment ouptut.

```
python -m easytext sentiment tmp/*.txt testoutput/sent_nonorm.xlsx --no-normalize
```
Make sentiment output using raw word counts


```
python -m easytext sentiment tmp/*.txt testoutput/sent_posneg.xlsx --posneg-only
```
Sentiment analysis oonly using positive/negative sentiment.



### Named Entity Recognition

Counts the number of times an entity appears in corpus documents.

**Entity Recognition Docs**

```
usage: __main__.py entities [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd]
                            [-m MIN_TF] [-hr] [-ut USE_TYPES]
                            [-it IGNORE_TYPES]
                            infiles [infiles ...] outfile

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

**Entity Recognition Examples**

```
python -m easytext entities tmp/*.txt testoutput/ent_m10.xlsx --min_tf 10
```
Count all entities that appear more than 10 times in the corpus.


```
python -m easytext entities tmp/*.txt testoutput/ent_usetypes.xlsx --min_tf 10 --use-types "PERSON,NORP"
```
Count all entities of types PERSON or NORM that appear more than 10 times in the corpus.


```
python -m easytext entities tmp/*.txt testoutput/ent_usetypes.xlsx --min_tf 10 --ignore-types "PERSON,NORP"
```
Count all entities of types other than PERSON or NORM that appear more than 10 times in the corpus.

**Entity Type Info**

These entity types are collected from Spacy's NER. The full page is here: https://spacy.io/api/annotation#named-entities


This is the table listed there:





### Topic Modeling

Performs LDA or NMF topic modeling on corpus using sklearn.

** Topic Modeling Help Docs **

```
usage: __main__.py topicmodel [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -n
                              NUMTOPICS [-t TYPE] [-s SEED] [-m MIN_TF]
                              [-nswm]
                              infiles [infiles ...] outfile

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

**Topic Modeling Examples**
```
python -m easytext topicmodel example_tmp/*.txt topicmodel_lda.xlsx --numtopics 10 --min_tf 5 --nosave_wordmatrix
```

Regular LDA topic model with 10 topics and excluding words that appear less than 5 times. Also doesn't save topic distribution to make a smaller file.

```
python -m easytext topicmodel example_tmp/*.txt topicmodel_nmf.xlsx --type NMF --numtopics 10 --min_tf 5 -nswm
```

Regular NMF topic model with 10 topics and excluding words that appear less than 5 times. Also doesn't save topic distribution to make a smaller file.

### GloVe Word Embedding

This function applies the GloVe word embedding space to a corpus, outputting both the raw word embeddings and a document vector estimation. In the future, this may be generalized to an embedding subcommand with doc2vec as another available option. It can also take keyword lists to hyper-rotate the embedding space so that each dimensions keywords create distinct 

**GloVe Word Embedding Help Docs**

```
usage: __main__.py glove [-h] [-dn DOCLABELCOL] [-c TEXTCOL] [-nhd] -d
                         DIMENSIONS [-kw KEYWORDS] [-s SEED] [-m MIN_TF]
                         [-nswm]
                         infiles [infiles ...] outfile
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

**GloVe Examples**

```
python -m easytext glove -d 10 tmp/*.txt testoutput/glove_10.xlsx
```
Glove model in 10 dimension embedding space.


```
python -m easytext glove -d 10 tmp/*.txt testoutput/glove_minct3.xlsx -m 3
```
Glove model in 10 dimension vector space excluding all words that appear less than 3 times in the corpus.


```
python -m easytext glove -d 10 tmp/*.txt testoutput/glove_nosavewm.xlsx --nosave_wordmatrix
```
Glove model in 10 dimensional vector space that doesn't include the word matrix to minimize output file size. If output size is too big, will save as .hdf which may be more difficult to work on depending on your application.

```
python -m easytext glove -d 10 tmp/*.txt testoutput/glove_all.xlsx --nosave_wordmatrix -m 3
```
Glove model in 10 dimensional vector space excluding vocab appearing at least 3 times and not saving word matrix (smaller output file).


```
python -m easytext glove -d 10 tmp/*.txt testoutput/glove_all.xlsx --nosave_wordmatrix -m 1 --keywords 'news|event,story'
```
Glove model in 10 dimensional vector space excluding vocab appearing at least 1 time and not saving word matrix (smaller output file) and with vector dimension 1 oriented on the word "news" and dimension 2 oriented towards "event" + "story" rejected from dimension 1. Experimental approach to supervised topic/vector extraction. Let me know if you have any better ideas for this.




