

# Easy Text Analysis

Text analysis for those of us that don't want to code.

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


### Topic Modeling


#### Topic Modeling Help Docs

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

#### Topic Modeling Examples
```
python -m easytext topicmodel example_tmp/*.txt topicmodel_lda.xlsx --numtopics 10 --min_tf 5 --nosave_wordmatrix
```

Regular LDA topic model with 10 topics and excluding words that appear less than 5 times. Also doesn't save topic distribution to make a smaller file.

**Non-negative Matrix Factorization Example command**
```
python -m easytext topicmodel example_tmp/*.txt topicmodel_nmf.xlsx --type NMF --numtopics 10 --min_tf 5 -nswm
```

Regular NMF topic model with 10 topics and excluding words that appear less than 5 times. Also doesn't save topic distribution to make a smaller file.

### GloVe Word Embedding

This function applies the GloVe word embedding space to a corpus, outputting both the raw word embeddings and a document vector estimation. In the future, this may be generalized to an embedding subcommand with doc2vec as another available option. It can also take keyword lists to hyper-rotate the embedding space so that each dimensions keywords create distinct 

#### GloVe Word Embedding Help Docs

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

#### GloVe Examples

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




