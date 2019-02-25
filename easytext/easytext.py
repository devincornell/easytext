
from .pipelines import *
from .algorithms import *


algorithm_options = ('lda', 'nmf', 'glove')
def create_algorithm_spreadsheet(alg, fname, topn, **kwargs):
    assert(alg in algorithm_options)
    if alg == 'lda':
        model = lda(**kwargs)
        sheetnames = (
            'doctopics',
            'topicwords',
            'docsummary',
            'topicsummary',
        )
    elif alg == 'nmf':
        model = nmf(**kwargs)
        sheetnames = (
            'doctopics',
            'topicwords',
            'docsummary',
            'topicsummary',
        )
    elif alg == 'glove':
        model = glove(**kwargs)
        sheetnames = (
            'docvectors',
            'vectorwords',
            'docsummary',
            'vectorsummary',
        )
    
    model.write_report(fname,topn,sheetnames)
        


# VVVVVVVVVVVVVVVVVVVV PIPELINE COMPONENTS VVVVVVVVVVVVVVVVVVVVVVV

ALL_COMPONENTS = {
    'wordlist':{'comp':ExtractWordListPipeline,'dep':[]},
    'sentlist':{'comp':ExtractSentListPipeline,'dep':[]},
    'prepositions':{'comp':ExtractPrepositionsPipeline,'dep':[]},
    'entlist':{'comp':ExtractEntListPipeline, 'dep':[]},
    'nounverbs':{'comp':ExtractNounVerbsPipeline, 'dep':[]},
    'entverbs':{'comp':ExtractEntVerbsPipeline, 'dep':[]},
}


class EasyTextPipeline():
    name = 'easytext'
    def __init__(self, nlp, enable=None, disable=None, **kwargs):
        if enable is not None:
            usepipe = set(enable)
        elif disable is not None:
            usepipe = list(ALL_COMPONENTS.keys())
            usepipe -= set(disable)
        else:
            usepipe = set(ALL_COMPONENTS.keys())
        
        # ensure correct pipe names
        self.components = dict()
        for pn in usepipe:
            if pn not in ALL_COMPONENTS.keys():
                raise Exception('invalid pipe name provided:', pn)
            self.components[pn] = ALL_COMPONENTS[pn]['comp'](nlp, **kwargs)
    
    def __call__(self, doc):
        for pnname,pcomp in self.components.items():
            pcomp.__call__(doc)
        
        return doc

def easyparse(nlp,texts,enable=None,**kwargs):
    '''
        Runs spacy parser loop only extracting data from enabled custom modules.
    '''
    
    # enable spacy pipelines
    previously_enabled = True
    if not 'easytext' in nlp.pipe_names:
        previously_enabled = False
        component = EasyTextPipeline(nlp,enable=enable,**kwargs)
        nlp.add_pipe(component,name='easytext')
        
    # extracts only easytext data from docs as generator
    for doc in nlp.pipe(texts, **kwargs):
        dat = doc._.easytext
        yield dat
        
    # removes if it wasn't previously added
    if not previously_enabled:
        nlp.remove_pipe('easytext')
    