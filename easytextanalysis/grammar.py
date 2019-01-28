from .ner import get_ent_obj
from collections import Counter


def getverb(tok):
    '''Finds the associated verb from a given noun token.
        tok: reference to a token of a doc which is 
            being navigated.
    '''
    if tok.dep_ == "nsubj" and tok.head.pos_ == 'VERB':
        return tok.head
    else:
        None
    #if tok.dep_ == "ROOT":
        # base case: reached tree root
    #if tok.pos_ in ("VERB", "ADV"):
    #    return tok
    #elif tok.dep_ == "ROOT":
    #    return None
    #else:
        #print(tok)
        #raise Exception('No verb was found in this parse.')
    #    return None
    #else:
    #    return getverb(tok.head)

def get_nounverb(noun):
    relations = list()
    verb = getverb(noun)
    if verb is not None:
    #    relations.append((noun,verb,))
        return (noun,verb)
    #return relations
    else:
        return None

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
    
    #docentcts = [dict(Counter(ents)) for ents in docents]
    
    return docents
    




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
                pp = ''.join([tok.orth_ + tok.whitespace_ for tok in token.subtree])
                phrases.append(pp)
        allphrases.append(phrases)
    
    ctphrases = [dict(Counter(ph)) for ph in allphrases]
    
    return ctphrases
    

    
    
    
    














