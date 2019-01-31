
from .ner import ExtractEntsPipeline
from .grammar import ExtractPrepositionsPipeline, ExtractNounVerbsPipeline, ExtractEntVerbsPipeline

class EasyTextPipeline():
    def __init__(self, enable=None, disable=None, use_ent_types=None):
        usepipe = {'ents', 'prepositions', 'nounverbs', 'entverbs'}
        if enable is not None:
            usepipe = set(enable)
        
        elif disable is not None:
            usepipe -= set(disable)
            
        self.pipe_components = list()
        if 'ents' in usepipe:
            self.pipe_components.append(ExtractEntsPipeline(use_ent_types))
            
        if 'prepositions' in usepipe:
            self.pipe_components.append(ExtractPrepositionsPipeline())
            
        if 'nounverbs' in usepipe:
            self.pipe_components.append(ExtractNounVerbsPipeline())
            
        if 'entverbs' in usepipe:
            self.pipe_components.append(ExtractEntVerbsPipeline())
        
    def __call__(self,doc):
        for pc in self.pipe_components:
            doc = pc.__call__(doc)
        
        return doc
    
    