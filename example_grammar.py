#whitespace_
#from tools import *
from easytext import *
import spacy

if __name__ == '__main__':
    
    # new spacy parser
    nlp = spacy.load('en')
    
    # open text files and read data
    with open('sampletexts/test.txt','r') as f:
        text = f.read()
    texts = [l for l in text.split('\n') if len(l) > 0]
    names = list(range(len(texts)))
    print(len(texts), 'texts found.')
    
    # parse all text documents
    docs = list(nlp.pipe(texts))
    
    # extract entity frequencies
    entlist, entmap = extract_entities(docs)
    print(entlist)
    print()
    
    # extract prepositional phrases
    preps = extract_prepositions(docs)
    print(preps)
    print()
    
    # extract noun-verb pairs
    nv = extract_nounverbs(docs)
    print(nv)
    print()
    
    # extract entity-verb pairs
    ev = extract_entverbs(docs)
    print(ev)
    print()
    