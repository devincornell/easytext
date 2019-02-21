from collections import Counter
from .pipelines import *


        

    
def extract_prepositions(docs, **kwargs):
    eep = ExtractPrepositionsPipeline(**kwargs)
    
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
    
    ppcts = [d._.prepphrasecounts for d in docs]
    return ppcts

def extract_nounverbs(docs, **kwargs):
    eep = ExtractNounVerbsPipeline(**kwargs)
    
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
    
    nvcts = [d._.nounverbcounts for d in docs]
    return nvcts
    
    
    
    

    
def extract_entverbs(docs, **kwargs):
    eep = ExtractEntVerbsPipeline(**kwargs)
    
    for doc in docs:
        # will modify doc object
        eep.__call__(doc)
    
    evcts = [d._.entverbcts for d in docs]
    return evcts

