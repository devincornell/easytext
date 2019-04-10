
from .pipelines import *

from collections import Counter
from spacy.tokens import Doc
import string



# VVVVVVVVVVVVVVVVVVVV PIPELINE COMPONENTS VVVVVVVVVVVVVVVVVVVVVVV

ALL_COMPONENTS = {
    'wordlist':{'comp':ExtractWordListPipeline,'dep':[]},
    'sentlist':{'comp':ExtractSentListPipeline,'dep':[]},
    'entlist':{'comp':ExtractEntListPipeline, 'dep':[]},
    'prepphrases':{'comp':ExtractPrepositionsPipeline,'dep':[]},
    'nounverbs':{'comp':ExtractNounVerbsPipeline, 'dep':[]},
    'entverbs':{'comp':ExtractEntVerbsPipeline, 'dep':['entlist',]},
    'nounphrases':{'comp':ExtractNounPhrasesPipeline, 'dep':[]},
}

# default args are consumed in pipeline components
DEFAULT_PIPE_ARGS = dict(use_ents=True, use_ent_types=None, ignore_ent_types=None) # defaults that can be written over
def easyparse(nlp,texts,enable=None,pipeargs=dict(),spacyargs=dict()):
    '''
        Runs spacy parser loop only extracting data from enabled custom modules.
        
        Output: Generator for each parsed document. Enabled features correspond to 
            dictionary keys here. For instance, if enable=['wordlist',],
            the generator output will add a key called 'wordlist'.
        
        Inputs:
            nlp: Spacy nlp objects, usually init by nlp = spacy.load('en')
            texts: iterable of raw text data as strings
            enable: list of pipeline components to use. Each component enables
                some data in the generated outputs, always corresponding to 
                the same name as the component itself (but sometimes the pipe 
                outputs include additional properties.
            pipeargs: Dictionary corresponding to arguments passed to pipeline
                components. Pipearg key->values might apply to one or more pipeline 
                component. For instance, the 'use_ents' flag combines multi-word 
                entities to both word lists and sent lists. See documentation for
                individual pipeline components to see the pipeargs used. Defaults
                are listed in the DEFAULT_PIPE_ARGS found above this fuction 
                definition.
            spacyargs: Arguments that, when unpacked, will be pased directly to 
                the spacy.pipe() method.
            
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
    '''
        Master pipeline that combines all EasyText pipeline components
            listed in ALL_COMPONENTS and defined in pipelines.py.
        Output: None. Attaches the property spacy doc._.easytext to
            all spacy doc objects.
        
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            enable: Enabled pipeline components. Default is to
                include all pipeline components.
            disable: Pipeline components not to include.
            pipeargs: pipeline args passed to each of the individ.
                pipeline components found in pipelines.py.
    '''
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


