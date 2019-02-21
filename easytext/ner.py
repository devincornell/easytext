from collections import Counter
from spacy.tokens import Doc
import string
from .pipelines import *

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
    
    