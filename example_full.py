#whitespace_
#from tools import *
import easytext as et
import spacy

if __name__ == '__main__':
    
    # open text files and read data
    with open('sampletexts/test.txt','r') as f:
        text = f.read()
    texts = [l for l in text.split('\n') if len(l) > 0]
    names = list(range(len(texts)))
    print(len(texts), 'texts found.')
    
    # add pipeline component and parse with spacy directly
    nlp = spacy.load('en',)
    nlp.add_pipe(et.EasyTextPipeline(nlp))
    print('pipeline components:', nlp.pipe_names)
    for doc in nlp.pipe(texts):
        print(doc._.easytext['entlist'])
        print()
    
    # OR, use .parse to extract just the easytext data
    nlp = spacy.load('en',)
    for dat in et.parse(nlp,texts):
        print(dat['entlist'])
        print()
    
    