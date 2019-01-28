#whitespace_

from easytextanalysis import *
import spacy

if __name__ == '__main__':
    text = 'Today I ran over the log with my car in the United States of America.'
    t2 = 'The United States said they wouldnt get involved.'
    
    nlp = spacy.load('en')
    
    docs = [nlp(text),nlp(t2),]
    
    
    #print(get_ents(docs))
    
    #print(get_prepositions([nlp(text),],nlp))
    
    print(get_ents(docs))
    print(get_entverbs(docs))
    print(get_prepositions(docs))
    