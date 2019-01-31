from collections import Counter
import string
from spacy.tokens import Doc
from .tools import count_totals



def getverb(tok):
    '''Finds the associated verb from a given noun token.
        tok: reference to a token of a doc which is 
            being navigated.
    '''
    if tok.dep_ == "nsubj" and tok.head.pos_ == 'VERB':
        return tok.head
    else:
        None
        
def get_nounverb(noun):
    relations = list()
    verb = getverb(noun)
    if verb is not None:
        return (noun,verb)
    else:
        return None


class ExtractPrepositionsPipeline():
    name = 'prepositions'
    def __init__(self):
        #self.phrases = list()
        Doc.set_extension('prepphrases', default=list())
        Doc.set_extension('prepphrasecounts', default=list())
        
    def __call__(self, doc):
        
        phrases = list()
        for tok in doc:
            if tok.pos_ == 'ADP':
                pp = ''.join([t.orth_ + t.whitespace_ for t in tok.subtree])
                phrases.append(pp)
        
        doc._.prepphrasecounts = dict(Counter(phrases))
        doc._.prepphrases = phrases
        
        return doc
    
def extract_prepositions(docs, **kwargs):
    eep = ExtractPrepositionsPipeline(**kwargs)
    
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
    
    ppcts = [d._.prepphrasecounts for d in docs]
    return ppcts
    

class ExtractNounVerbsPipeline():
    name = 'nounverbs'
    def __init__(self):
        #self.phrases = list()
        Doc.set_extension('nounverbs', default=list())
        Doc.set_extension('nounverbcounts', default=list())
        
    def __call__(self, doc):
        
        #for span in list(doc.noun_chunks):
        #    span.merge()
        
        nounverbs = list()
        for tok in doc:
            if tok.pos_ in ('PROPN', 'NOUN'):
                nv = get_nounverb(tok)
                if nv is not None:
                    nounverbs.append((nv[0].text, nv[1].text))
        
        doc._.nounverbcounts = dict(Counter(nounverbs))
        doc._.nounverbs = nounverbs
        
        return doc

def extract_nounverbs(docs, **kwargs):
    eep = ExtractNounVerbsPipeline(**kwargs)
    
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
    
    nvcts = [d._.nounverbcounts for d in docs]
    return nvcts
    
    
    
    
    
    
class ExtractEntVerbsPipeline():
    name = 'entverbs'
    def __init__(self,):
        Doc.set_extension('entverbs', default=list())
        Doc.set_extension('entverbcts', default=list())
        
    def __call__(self, doc):
        # merge multi-word entities
        spans = list(doc.ents)
        for span in spans:
            span.merge()
        
        
        entverbs = list()
        for ename, eobj in doc._.entlist:
            nv = get_nounverb(eobj)
            if nv is not None:
                entverbs.append((nv[0].text, nv[1].text))
        
        doc._.entverbs = entverbs
        doc._.entverbcts = dict(Counter(entverbs))
        
        return doc
    
def extract_nounverbs(docs, **kwargs):
    eep = ExtractEntVerbsPipeline(**kwargs)
    
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
    
    evcts = [d._.entverbcts for d in docs]
    return evcts

