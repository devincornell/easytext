from collections import Counter
from spacy.tokens import Doc
import string

def get_basetext(etext):
    # (i.e. combine "US" with "U.S.")
    rmpunc_table = etext.maketrans('','', string.punctuation)
    rmpunct = etext.translate(rmpunc_table)
    basetext = rmpunct.upper().replace(' ','')
    return basetext


class ExtractEntsPipeline():
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


def extract_entities(docs, **kwargs):
    eep = ExtractEntsPipeline(**kwargs)
    entmap = None
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
        
        # we want the entmap from the last doc
        entmap = doc._.entmap
    
    #entlists = [d._.entlist for d in docs]
    #entmaps = [d._.entmap for d in docs]
    entcts = [d._.entcts for d in docs]
    return entcts, entmap
    
    