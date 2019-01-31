#whitespace_
#from tools import *
from easytextanalysis import *
import spacy

if __name__ == '__main__':
    
    # add easytext pipeline component to new spacy parser
    nlp = spacy.load('en')
    et = EasyTextPipeline()
    nlp.add_pipe(et, last=True)
    

    names = ('a','b')
    t1 = 'Today I ran over the log with my car in the United States of America. The U.S. went to the store. I went to the hat.'
    t2 = 'The United States said they wouldnt get involved. Russia attacked Canada.'
    texts = [t1,t2]
    
    
    entcts = list()
    prepcts = list()
    nvcts = list()
    evcts = list()
    for name, doc in zip(names, nlp.pipe(texts)):
        #print(doc._.entlist)
        #entmap
        #entcts
        entcts.append(doc._.entcts)
        
        #print(doc._.prepphrases)
        #prepphrasecounts
        prepcts.append(doc._.prepphrasecounts)
        
        #print(doc._.nounverbs)
        #nounverbcounts
        nvcts.append(doc._.nounverbcounts)
        
        #print(doc._.entverbs)
        #entverbcts
        evcts.append(doc._.entverbcts)
        
        #print()
        
    entdf = dict2df(entcts, names)
    #entdf.append(count_totals(entcts))
    
    prepdf = dict2df(prepcts, names)
    nvdf = dict2df(nvcts, names)
    evdf = dict2df(evcts, names)
    print(entdf)