from collections import Counter
import string
from .tools import count_totals


def get_basetext(etext):
    # (i.e. combine "US" with "U.S.")
    rmpunc_table = etext.maketrans('','', string.punctuation)
    rmpunct = etext.translate(rmpunc_table)
    basetext = rmpunct.upper().replace(' ','')
    return basetext


def get_ent_obj(docs, use_ent_types=None):
    '''
        Extracts entity names and objects, combining names that are same after removing punctuation and
            capitalization.
        Inputs:
            docs: list of Spacy document objects.
        Output:
            - list of entities as strings for each document and counts
            - total counts across all documents
    '''
    
    allents = list()
    entmap = dict() # basetext -> list(entnames)
    for doc in docs:
        
        spans = list(doc.ents)
        for span in spans:
            span.merge()
        
        if use_ent_types is None:
            ents = [e for e in doc if e.ent_type > 0]
        else:
            ents = [e for e in doc if e.ent_type > 0 and e.ent_id_ in use_ent_types]
        
        for i in range(len(ents)):
            basetext = get_basetext(ents[i].text)
            
            if basetext not in entmap.keys():
                entmap[basetext] = [ents[i].text,]
            
            elif ents[i].text not in entmap[basetext]:
                entmap[basetext].append(ents[i].text)
                
            ents[i] = (entmap[basetext][0],ents[i])
                       
        allents.append(ents)
                       
    return allents


def get_ents(docs, use_ent_types=None):
    '''
        Extracts entity names, combining names that are same after removing punctuation and
            capitalization.
        Inputs:
            docs: list of Spacy document objects.
        Output:
            - list of prepositional phrases as strings for each document and counts
            - total counts across all documents
    '''
    
    docentobj = get_ent_obj(docs, use_ent_types)
    
    #combine doc entity totals
    entcts = list()
    for ents in docentobj:
        entct = dict(Counter([n for n,e in ents]))
        entcts.append(entct)
    
    #combine doc entity totals
    #totals = dict()
    #for ect in entcts:
    #    for e,ct in ect.items():
    #        if e not in totals:
    #            totals[e] = 0
    #        totals[e] += ct
    totals = count_totals(entcts)
        
    return entcts, totals



'''


        tokseq = list()
        ents = list()
        for tok in doc:
            #print(tok, tok.ent_type)
            if tok.ent_type in USE_ENT_IOB:
                basetext = get_basetext(tok.text)
                
                if basetext not in entmap.keys():
                    entmap[basetext] = [tok.text,]
                    
                elif tok.text not in entmap[basetext]:
                    entmap[basetext].append(tok.text)
                    
                # add the first identified entity name to X
                tokseq.append(entmap[basetext][0] + '*')
                ents.append(entmap[basetext][0] + '*')
                
            else:
                # token is regular text
                tokseq.append(tok.lower_)


'''

