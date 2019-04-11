
# EasyText

This package combines several common text analysis algorithms into a single interface. It includes a simple interface for parsing text data through an API driven by custom Spacy pipeline components and an extensive command-line interface which wraps the EasyText api and other features. This document will cover primarily the Python API; for command line reference, see the documentation on the [Command Reference Page](/docs/Command_Reference.md)).

The easytext interface can be divided into two sections: pre-processing with the `easyparse()` function and algorithm wrapper functions.

## Preprocessing Using `easyparse()` Function

The preprocessing features of EasyText can be accessed through the `easyparse()` function, which is primarily a wrapper around the `spacy.pipe()` method with custom pipeline components that accomplish common tasks. As a preliminary example, the basic workflow is to (1) acquire the texts as a list of strings (`texts` variable in this example), (2) choose the easyparse features you would like to enable, (3) call the `easyparse()` function in a loop, and (4) consume the resulting data. The following example shows a simple example using the 'wordlist' and 'entlist' features of EasyText.

```
from easytext import easyparse

texts # list of strings containing the texts of interest

nlp = spacy.load('en')
for etdoc in easyparse(nlp, texts, enable=['wordlist','entlist']):
    print(etdoc['wordlist'])
    print(etdoc['entlist'], end='\n\n')
```

### Preprocessing Feature List

The full list of preprocessing components is provided below. Each component has an associated output variable of the same name that will appear as a key in the document dictionary output from the `easyparse()` function. These components are enabled by using the `enable` keyword argument to the `easytext()` function. For instance, if I wanted to get a list of named entities and noun-verb pairs from a set of documents, I would use the `easytext()` argument `enable = ['entlist', 'nounverbs']`, when could then be accessed using the 'entlist' and 'nounverb' entries in the returned document data.

* **wordlist**: Extracts a list of tokens, including words and punctuation, that appear in the document.
* **sentlist**: Contains a list of sentence token lists that appear in the document.
* **entlist**: Contains a list of named entities observed in the document. Named entities are combined if they have the same representation after changing to lower case and removing whitespace.
* **prepphrases**: List of prepositional phrases found in the document.
* **nounverbs**: List of (noun, verb) pair tuples found in the document.
* **entverbs**: List of (entity, verb) pair tuples found in the document.
* **nounphrases**: List of nouns and noun phrases found in the document.

## Algorithm Wrapper Functions

In addition to convenient preprocessing commands, EasyText offers a series of algorithms that follow a typical form but wrap algorithms from multiple packages. These algorithms all return document representations either in terms of topic distributions or embedding vector representations.

* **lda**: Implements a wrapper around sklearn LatentDirichletAllocation algorithm.
* **nmf**: Implements a wrapper around sklearn NMF algorithm.
* **glove**: Implements wrapper around python-glove package for creating word embeddings.

The following code uses the lda function with the `easytext()` preprocessor to generate a topic model with 10 topics.

```
from easytext import easyparse

texts # list of strings containing the texts of interest

# preprocess documents into bags of words
nlp = spacy.load('en')
docbows = list()
for etdoc in easyparse(nlp, texts, enable=['wordlist',]):
    docbows.append(etdoc['wordlist'])

# create topic model
topicmodel = lda(docbows, 10)

# print topics most closely associated with each document
print(topicmodel.doc_feature_summary(topn=5))
```
