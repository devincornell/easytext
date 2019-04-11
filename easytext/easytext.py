
from .pipelines import *

from collections import Counter
from spacy.tokens import Doc
import string



# VVVVVVVVVVVVVVVVVVVV PIPELINE COMPONENTS VVVVVVVVVVVVVVVVVVVVVVV

# NOTE NOTE NOTE: Do not have circular dependenceies "OR ELSE."
ALL_COMPONENTS = {
    'wordlist':{'comp':ExtractWordListPipeline,'easytext_dep':[], 'spacy_dep':['sbd',]},
    'sentlist':{'comp':ExtractSentListPipeline,'easytext_dep':[], 'spacy_dep':['sbd',]},
    'entlist':{'comp':ExtractEntListPipeline, 'easytext_dep':[], 'spacy_dep':['ner','parser']},
    'prepphrases':{'comp':ExtractPrepositionsPipeline,'easytext_dep':[], 'spacy_dep':[]},
    'nounverbs':{'comp':ExtractNounVerbsPipeline, 'easytext_dep':[], 'spacy_dep':[]},
    'entverbs':{'comp':ExtractEntVerbsPipeline, 'easytext_dep':['entlist',], 'spacy_dep':[]},
    'nounphrases':{'comp':ExtractNounPhrasesPipeline, 'easytext_dep':[], 'spacy_dep':[]},
}

def recursive_add_component(add_component, components, nlp, pipeargs):
    '''
        Recursively adds pipelines to spacy nlp model, ensuring both spacy and easytext 
            dependencies are met.
        
        Output: Generator for each parsed document. Enabled features correspond to 
            dictionary keys here. For instance, if enable=['wordlist',],
            the generator output will add a key called 'wordlist'.
        
        Inputs:
            add_component: str name of component to add, out of components.keys()
            components: dictionary of easytext component names and objects with
                easytext ('easytext_dep') and spacy ('spacy_dep') dependencies.
            nlp: spacy model to add pipelines to.
            
    '''
    
    if add_component not in nlp.pipe_names:
        comp = components[add_component]

        # add in other EasyText depenencies
        for etdep in comp['easytext_dep']:
            if etdep not in nlp.pipe_names:
                nlp = recursive_add_component(etdep, components, nlp, pipeargs)

        # add in spacy dependencies
        for sdep in comp['spacy_dep']:
            if sdep not in nlp.pipe_names:
                new_comp = nlp.create_pipe(sdep)
                nlp.add_pipe(new_comp, last=True)

        # actually add current component
        nlp.add_pipe(comp['comp'](nlp, pipeargs), name=add_component, last=True)
    
    return nlp

# default args are consumed in pipeline components
DEFAULT_PIPE_ARGS = dict(use_ents=False, use_ent_types=None, ignore_ent_types=None) # defaults that can be written over
def easyparse(nlp,texts,enable=None, disable=None, pipeargs=dict(),spacyargs=dict()):
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
    
    # remove all existing pipe components
    for pname in nlp.pipe_names:
        if pname in ALL_COMPONENTS.keys():
            nlp.remove_pipe(pname)
    
    # choose which components to activate
    if enable is not None:
        usepipes = set(enable)
    elif disable is not None:
        usepipes = list(ALL_COMPONENTS.keys())
        usepipes -= set(disable)
    else:
        usepipes = set(ALL_COMPONENTS.keys())
    
    # error check applied pipes
    if not all([p in ALL_COMPONENTS.keys() for p in usepipes]):
        raise Exception('Not all of', usepipes, 'are EasyText pipeline names.')
    
    # add all components, recursing through dependency trees
    for pipename in usepipes:
        nlp = recursive_add_component(pipename, ALL_COMPONENTS, nlp, pipeargs)
    
    # extracts only easytext data from docs as generator
    for doc in nlp.pipe(texts, **spacyargs):
        dat = doc._.easytext
        yield dat
