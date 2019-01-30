from collections import Counter
from spacy.tokens import Doc
import string

def get_basetext(etext):
    # (i.e. combine "US" with "U.S.")
    rmpunc_table = etext.maketrans('','', string.punctuation)
    rmpunct = etext.translate(rmpunc_table)
    basetext = rmpunct.upper().replace(' ','')
    return basetext


class ExtractEnts():
    name = 'entities'
    def __init__(self, use_ent_types=None):
        #self.allents = list()
        self.use_ent_types = use_ent_types
        self.entmap = dict() # basetext -> list(entnames)
        
        # these will be set by spacy in the pipeline
        Doc.set_extension('entlist', default=list())
        Doc.set_extension('entmap', default=dict())
        Doc.set_extension('entcts', default=dict())
        

    def __call__(self, doc):
        
        # merge multi-word entities
        spans = list(doc.ents)
        for span in spans:
            span.merge()

        # extract entities
        if self.use_ent_types is None:
            ents = [e for e in doc if e.ent_type > 0]
        else:
            ents = [e for e in doc if e.ent_type > 0 and e.ent_id_ in self.use_ent_types]
        
        # combine entities if they have same basetext
        for i in range(len(ents)):
            basetext = get_basetext(ents[i].text)
            
            if basetext not in self.entmap.keys():
                self.entmap[basetext] = [ents[i].text,]
            
            elif ents[i].text not in self.entmap[basetext]:
                self.entmap[basetext].append(ents[i].text)
                
            ents[i] = (self.entmap[basetext][0],ents[i])
                       
        # count entities in this list
        entcts = dict(Counter([n for n,e in ents]))
        
        # set properties into pipeline
        doc._.entlist = ents
        doc._.entmap = self.entmap
        doc._.entcts = entcts
        
        return doc



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
    
    totals = count_totals(entcts)
        
    return entcts, totals