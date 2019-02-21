
from spacy.tokens import Doc
import string
from collections import Counter

class ExtractWordListPipeline():
    #name = 'easytext-wordlist'
    def __init__(self,nlp):
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
        
    def __call__(self, doc):
        
        usetok = lambda t: t.is_alpha or (t.text[0] == "'" and t.text[1:].isalpha())
        wordlist = [t.lower_ for t in doc if usetok(t)]
        
        doc._.easytext['wordlist'] = wordlist
        
        return doc

class ExtractPrepositionsPipeline():
    #name = 'easytext-prepositions'
    def __init__(self,nlp):
        
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())        
    def __call__(self, doc):
        
        phrases = list()
        for tok in doc:
            if tok.pos_ == 'ADP':
                pp = ''.join([t.orth_ + t.whitespace_ for t in tok.subtree])
                phrases.append(pp)
        
        doc._.easytext['prepphrasecounts'] = dict(Counter(phrases))
        doc._.easytext['prepphrases'] = phrases
        
        return doc
    
    
def get_nounverb(noun):
    relations = list()
    verb = getverb(noun)
    if verb is not None:
        return (noun,verb)
    else:
        return None
    
class ExtractNounVerbsPipeline():
    #name = 'easytext-nounverbs'
    def __init__(self,nlp):
        #self.phrases = list()
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())        
    def __call__(self, doc):
        
        #for span in list(doc.noun_chunks):
        #    span.merge()
        
        nounverbs = list()
        for tok in doc:
            if tok.pos_ in ('PROPN', 'NOUN'):
                nv = get_nounverb(tok)
                if nv is not None:
                    nounverbs.append((nv[0].text, nv[1].text))
        
        doc._.easytext['nounverbcounts'] = dict(Counter(nounverbs))
        doc._.easytext['nounverbs'] = nounverbs
        
        
        return doc
    
    
def getverb(tok):
    '''Finds the associated verb from a given noun token.
        tok: reference to a token of a doc which is 
            being navigated.
    '''
    if tok.dep_ == "nsubj" and tok.head.pos_ == 'VERB':
        return tok.head
    else:
        None
    
class ExtractEntVerbsPipeline():
    #name = 'easytext-entverbs'
    def __init__(self,nlp):
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
        
        if not 'easytext-entlist' in nlp.pipe_names:
            component = ExtractEntListPipeline(nlp)
            nlp.add_pipe(component,last=True)
            
    def __call__(self, doc):
        # merge multi-word entities
        spans = list(doc.ents)
        for span in spans:
            span.merge()
        
        
        entverbs = list()
        for ename, eobj in doc._.easytext['entlist']:
            nv = get_nounverb(eobj)
            if nv is not None:
                entverbs.append((nv[0].text, nv[1].text))
        
        doc._.easytext['entverbs'] = entverbs
        doc._.easytext['entverbcts'] = dict(Counter(entverbs))
        
        return doc
    
    
def get_basetext(etext):
    # (i.e. combine "US" with "U.S.")
    rmpunc_table = etext.maketrans('','', string.punctuation)
    rmpunct = etext.translate(rmpunc_table)
    basetext = rmpunct.upper().replace(' ','')
    return basetext

class ExtractEntListPipeline():
    #name = 'easytext-entlist'
    def __init__(self, nlp, use_ent_types=None):
        #self.allents = list()
        self.use_ent_types = use_ent_types
        self.entmap = dict() # basetext -> list(entnames)
        
        # these will be set by spacy in the pipeline
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())        

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
        doc._.easytext['entlist'] = ents
        doc._.easytext['entmap'] = self.entmap
        doc._.easytext['entcts'] = entcts
        
        return doc