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
    
    

def get_entverbs(docs, use_ent_types=None):
    entobj = get_ent_obj(docs, use_ent_types)
    
    docents = list()
    for ents in entobj:
        nounverbs = list()
        for ename,eobj in ents:
            nv = get_nounverb(eobj)
            if nv is not None:
                nounverbs.append((nv[0].text, nv[1].text))
        
        docents.append(dict(Counter(nounverbs)))
    
    totcts = count_totals(docents)
    #docentcts = [dict(Counter(ents)) for ents in docents]
    
    return docents, totcts


def get_prepositions(docs):
    '''
        Extracts prepositional phrases from list of Spacy doc objects.
        Inputs:
            docs: list of Spacy document objects.
        Output:
            list of prepositional phrases as strings for each document and counts
    '''
    allphrases = list()
    for doc in docs:
        phrases = list()
        for token in doc:
            if token.pos_ == 'ADP':
                pp = ''.join([tok.text + tok.whitespace_ for tok in token.subtree])
                phrases.append(pp)
                print(pp)
        allphrases.append(phrases)
    
    ctphrases = [dict(Counter(ph)) for ph in allphrases]
    totcts = count_totals(ctphrases)
    
    return ctphrases, totcts









def get_entverbs(docs, use_ent_types=None):
    entobj = get_ent_obj(docs, use_ent_types)
    
    docents = list()
    for ents in entobj:
        nounverbs = list()
        for ename,eobj in ents:
            nv = get_nounverb(eobj)
            if nv is not None:
                nounverbs.append((nv[0].text, nv[1].text))
        
        docents.append(dict(Counter(nounverbs)))
    
    totcts = count_totals(docents)
    #docentcts = [dict(Counter(ents)) for ents in docents]
    
    return docents, totcts
    



