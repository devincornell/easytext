#whitespace_
#from tools import *
from easytextanalysis import *
import spacy

if __name__ == '__main__':
    text = 'Today I ran over the log with my car in the United States of America. The U.S. went to the store. I went to the hat.'
    t2 = 'The United States said they wouldnt get involved. Russia attacked Canada.'
    
    nlp = spacy.load('en')
    
    docs = [nlp(text),nlp(t2),]
    names = ('a','b')
    
    nlp = spacy.load('en')
    component = ExtractEnts()
    nlp.add_pipe(component, after='ner')
    
    c = ExtractPrepositions()
    nlp.add_pipe(c, after='parser')
    
    c = ExtractNounVerbs()
    nlp.add_pipe(c, after='parser')
    
    c = ExtractEntVerbs()
    nlp.add_pipe(c, after='parser')
    
    for doc in nlp.pipe([text,t2]):
        print(doc._.entlist)
        print(doc._.prepphrases)
        print(doc._.nounverbs)
        print(doc._.entverbs)
        print()
    exit()
    #exit()
    
    #print(get_ents(docs))
    
    #print(get_prepositions([nlp(text),],nlp))
    
    #print(get_ents(docs))
    #print(get_entverbs(docs))
    #print(get_prepositions(docs))
    
    #entcts, enttots = get_ents(docs)
    #print(dict2df(entcts,names))
    #print()
    
    #entcts, enttots = get_entverbs(docs)
    #print(dict2df(entcts,names))
    #print()
    
    #entcts, enttots = get_prepositions(docs)
    #print(entcts)
    #print(dict2df(entcts,names))
    #print()
    
    
    #print(enttots)
    #print()
    
    
    