#whitespace_
#from tools import *
from easytext import *
import spacy

if __name__ == '__main__':
    
    # add easytext pipeline component to new spacy parser
    nlp = spacy.load('en')
    #et = EasyTextPipeline()
    #nlp.add_pipe(et, last=True)
    


    #t1 = 'Today I ran over the log with my car in the United States of America. The U.S. went to the store. I went to the hat.'
    #t2 = 'The United States said they wouldnt get involved. Russia attacked Canada.'
    #texts = [t1,t2]
    
    with open('sampletexts/test.txt','r') as f:
        text = f.read()
    texts = [l for l in text.split('\n') if len(l) > 0]
    names = list(range(len(texts)))
    print(len(texts), 'texts found.')
    
    docs = list(nlp.pipe(texts))
    
    entlist, entmap = extract_entities(docs)
    print(entlist)
    print()
    
    preps = extract_prepositions(docs)
    print(preps)
    print()
    
    nv = extract_nounverbs(docs)
    print(nv)
    print()
    
    ev = extract_entverbs(docs)
    print(ev)
    print()
    
        
    #entdf = dict2df(entcts, names)
    #entdf.append(count_totals(entcts))
    
    #prepdf = dict2df(prepcts, names)
    #nvdf = dict2df(nvcts, names)
    #evdf = dict2df(evcts, names)
    #print(entdf)