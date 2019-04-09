
from .pipelines import *

from collections import Counter
from spacy.tokens import Doc
import string



# VVVVVVVVVVVVVVVVVVVV PIPELINE COMPONENTS VVVVVVVVVVVVVVVVVVVVVVV

ALL_COMPONENTS = {
    'wordlist':{'comp':ExtractWordListPipeline,'dep':[]},
    'sentlist':{'comp':ExtractSentListPipeline,'dep':[]},
    'entlist':{'comp':ExtractEntListPipeline, 'dep':[]},
    'prepositions':{'comp':ExtractPrepositionsPipeline,'dep':[]},
    'nounverbs':{'comp':ExtractNounVerbsPipeline, 'dep':[]},
    'entverbs':{'comp':ExtractEntVerbsPipeline, 'dep':['entlist',]},
    'nounphrases':{'comp':ExtractNounPhrasesPipeline, 'dep':[]},
}

DEFAULT_PIPE_ARGS = dict(use_ents=True, use_ent_types=None, ignore_ent_types=None) # defaults that can be written over
def easyparse(nlp,texts,enable=None,pipeargs=dict(),spacyargs=dict()):
    '''
        Runs spacy parser loop only extracting data from enabled custom modules.
    '''
    pipeargs = {**DEFAULT_PIPE_ARGS, **pipeargs} # allows user to override defaults
    
    # enable spacy pipelines 
    previously_enabled = True
    if not 'easytext' in nlp.pipe_names:
        previously_enabled = False
        component = EasyTextPipeline(nlp,enable=enable,pipeargs=pipeargs)
        nlp.add_pipe(component,name='easytext')
        
    # extracts only easytext data from docs as generator
    for doc in nlp.pipe(texts, **spacyargs):
        dat = doc._.easytext
        yield dat
        
    # removes if it wasn't previously added
    if not previously_enabled:
        nlp.remove_pipe('easytext')

class EasyTextPipeline():
    name = 'easytext'
    def __init__(self, nlp, enable=None, disable=None, pipeargs=dict()):
        pipeargs = {**DEFAULT_PIPE_ARGS, **pipeargs} # allows user to override defaults
        
        if enable is not None:
            usepipe = set(enable)
        elif disable is not None:
            usepipe = list(ALL_COMPONENTS.keys())
            usepipe -= set(disable)
        else:
            usepipe = set(ALL_COMPONENTS.keys())
        
        # ensure correct pipe names
        self.components = list()
        for pn in usepipe:
            if pn not in ALL_COMPONENTS.keys():
                raise Exception('invalid pipe name provided:', pn)
            
            # add any dependencies before the listed component
            for dep in ALL_COMPONENTS[pn]['dep']:
                if not dep in [cname for cname,comp in self.components]:
                    self.components.append((dep, ALL_COMPONENTS[dep]['comp'](nlp,pipeargs)))
                
            # add component itself
            self.components.append((pn, ALL_COMPONENTS[pn]['comp'](nlp,pipeargs)))
    
    def __call__(self, doc):
        for pnname,pcomp in self.components:
            pcomp.__call__(doc)
        
        return doc


