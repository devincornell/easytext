
#from .ner import ExtractEntsPipeline
#from .grammar import ExtractPrepositionsPipeline, ExtractNounVerbsPipeline, ExtractEntVerbsPipeline
from .pipelines import *

#ALL_OPTIONS = ['ents','prepositions','nounverbs','entverbs']


# list of all pipeline components
ALL_COMPONENTS = {
    'wordlist':{'comp':ExtractWordListPipeline,'dep':['entlist',]},
    'prepositions':{'comp':ExtractPrepositionsPipeline,'dep':[]},
    'entlist':{'comp':ExtractEntListPipeline, 'dep':[]},
    'nounverbs':{'comp':ExtractNounVerbsPipeline, 'dep':[]},
    'entverbs':{'comp':ExtractEntVerbsPipeline, 'dep':[]},
}
#PIPENAME_PREFIX = 'easytext-'

class EasyTextPipeline():
    name = 'easytext'
    def __init__(self, nlp, enable=None, disable=None, **kwargs):
        if enable is not None:
            usepipe = set(enable)
        elif disable is not None:
            usepipe -= set(disable)
        else:
            usepipe = set(ALL_COMPONENTS.keys())
        
        # ensure correct pipe names
        self.components = dict()
        for pn in usepipe:
            if pn not in ALL_COMPONENTS.keys():
                raise Exception('invalid pipe name provided:', pn)
            self.components[pn] = ALL_COMPONENTS[pn](nlp, **kwargs)
    
    def __call__(self, doc):
        for pnname,pcomp in self.components.items():
            pcomp.__call__(doc)
        
        return doc

def parse(nlp,texts,enable=None,**kwargs):
    '''
        Runs spacy parser loop only extracting data from enabled custom modules.
    '''
    # enable spacy pipelines
    if not 'easytext' in nlp.pipe_names:
        comps = [en for en in enable if en in ALL_COMPONENTS.keys()]
        component = EasyTextPipeline(nlp,comps,**kwargs)
        nlp.add_pipe(component,name='easytext')
        
    # extracts only easytext data from docs as generator
    for doc in nlp.pipe(texts, **kwargs):
        dat = doc._.easytext
        yield 

    
    