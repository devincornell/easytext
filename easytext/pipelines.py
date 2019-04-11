
from spacy.tokens import Doc
import string
from collections import Counter
import spacy

    
# ________________________ Pipeline Component Definitions __________________________

# criteria to keep token (allows for tokens that begin with apostrophie)
# used in ExtractWordListPipeline and ExtractSentListPipeline
def use_token(tok):
    return tok.is_alpha or (tok.text[0] == "'" and tok.text[1:].isalpha())

def combine_ent_tokens(doc):
    # got code from internet
    for ent in doc.ents:
        ent.merge(tag=ent.root.tag_, ent_type=ent.root.ent_type_)
    

class ExtractWordListPipeline():
    #name = 'easytext-wordlist'
    '''
        Extracts word lists from each document. This can be used
            for input into topic modeling or other document-word-
            sequence or BoW algorithms.
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component.
                kwargs['use_ents']: combine multi-word entities.
    '''
    def __init__(self,nlp, kwargs):
        self.use_ents = kwargs['use_ents']
        
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
        
        if self.use_ents:
            self.usetext = lambda t: t.lower_ if t.ent_type_=='' else t.text
        else:
            self.usetext = lambda t: t.lower_
        
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
            
            
    def __call__(self, doc):
        
        # to combine entities
        if self.use_ents:
            combine_ent_tokens(doc)
        
        wordlist = [self.usetext(t) for t in doc if use_token(t)]
        
        doc._.easytext['wordlist'] = wordlist
        #doc._.easytext['wordcounts'] = dict(Counter(wordlist))
        
        return doc
    
class ExtractSentListPipeline():
    '''
        Extracts sentence lists from each document. This can be used
            for input into word embedding or other algorithms relying
            on sentence lists.
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component.
                kwargs['use_ents']: combine multi-word entities.
    '''
    #name = 'easytext-wordlist'
    def __init__(self,nlp, kwargs):
        self.use_ents = kwargs['use_ents']
        
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
            
            
        if self.use_ents:
            self.usetext = lambda t: t.lower_ if t.ent_type_=='' else t.text
        else:
            self.usetext = lambda t: t.lower_
            
        
    def __call__(self, doc):
        
        
        if self.use_ents:
            combine_ent_tokens(doc)
        
        sentlist = [[self.usetext(t) for t in s if use_token(t)] for s in doc.sents]
        
        doc._.easytext['sentlist'] = sentlist
        
        return doc

# --------------------------------- MOSTLY NER FOCUSED -----------------------------------
    
def get_basetext(etext):
    # (i.e. combine "US" with "U.S.")
    rmpunc_table = etext.maketrans('','', string.punctuation)
    rmpunct = etext.translate(rmpunc_table)
    basetext = rmpunct.upper().replace(' ','')
    return basetext

class ExtractEntListPipeline():
    #name = 'easytext-entlist'
    '''
        Extracts entity lists from each document, combining entities
            who have the same base text, or letter case and spacing
            (see get_basetext() for rules on base text).
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component.
                kwargs['use_ent_types']: entity types to include
                    in returned entity lists. Mut. exclusive with
                    'ignore_ent_types'.
                kwargs['ignore_ent_types']: entity types to exclude
                    in returned entity lists. Mut. exclusive with
                    'use_ent_types'.
    '''
    def __init__(self, nlp, kwargs):
        
        self.use_ent_types = kwargs['use_ent_types']
        self.ignore_ent_types = kwargs['ignore_ent_types']
        
        self.entmap = dict() # basetext -> list(entnames)
        
        # these will be set by spacy in the pipeline
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())        

    
    def __call__(self, doc):
        
        # merge multi-word entities
        spans = list(doc.ents)
        for span in spans:
            span.merge()

        # extract entities that meet conditions
        is_ent = lambda e: e.ent_type > 0 and len(e.text.strip()) > 0
        if self.use_ent_types is None and self.ignore_ent_types is None:
            ents = [e for e in doc if is_ent(e)]
        elif self.use_ent_types is not None:
            ents = [e for e in doc if is_ent(e) and e.ent_type_ in self.use_ent_types]
        elif self.ignore_ent_types is not None:
            ents = [e for e in doc if is_ent(e) and e.ent_type_ not in self.ignore_ent_types]
        else:
            raise Exception('shoot - logical error here')
        
        # combine entities if they have same basetext
        entdat = list()
        for ent in ents:
            basetext = get_basetext(ent.text)
            
            if basetext not in self.entmap.keys():
                self.entmap[basetext] = [ent.text,]
            
            elif ent.text not in self.entmap[basetext]:
                self.entmap[basetext].append(ent.text)
                
            entdat.append( (self.entmap[basetext][0],ent) )
            
        # count entities in this list
        entcts = dict(Counter([n for n,e in entdat]))
        
        # set properties into pipeline
        doc._.easytext['entlist'] = entdat
        doc._.easytext['entmap'] = self.entmap
        #doc._.easytext['entcts'] = entcts
        
        return doc
    
# ------------------------------- GRAMMAR FOCUSED PIPELINES ------------------------------

class ExtractPrepositionsPipeline():
    #name = 'easytext-prepositions'
    '''
        Extracts lists of prepositional phrases from each document.
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component. Currently unused.
    '''
    def __init__(self,nlp, kwargs):
        
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())        
    def __call__(self, doc):
        
        phrases = list()
        for tok in doc:
            if tok.pos_ == 'ADP':
                pp = ''.join([t.orth_ + t.whitespace_ for t in tok.subtree])
                phrases.append(pp)
        
        #doc._.easytext['prepphrasecounts'] = dict(Counter(phrases))
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
    '''
        Extracts noun-verb pair tuples from each document.
        Output: list of noun-verb pair tuples in the given document.
        
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component. Currently unused.
    '''
    def __init__(self,nlp, kwargs):
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
        
        #doc._.easytext['nounverbcounts'] = dict(Counter(nounverbs))
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
    '''
        Extracts entity-verb pair tuples from each document.
        Output: list of noun-verb pair tuples in the given document.
        
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component. In this pipeline, is passed
                directly to the ExtractEntListPipeline pipeline
                component.
    '''
    def __init__(self,nlp, kwargs):
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
            
    def __call__(self, doc):
        # merge multi-word entities
        spans = list(doc.ents)
        for span in spans:
            span.merge()
        
        entverbs = list()
        for ename, eobj in doc._.easytext['entlist']:
            nv = get_nounverb(eobj)
            if nv is not None:
                entverbs.append((nv[0].text.strip(), nv[1].text.strip()))
        
        doc._.easytext['entverbs'] = entverbs
        #doc._.easytext['entverbcts'] = dict(Counter(entverbs))
        
        return doc
    
    


class ExtractNounPhrasesPipeline():
    #name = 'easytext-prepositions'
    '''
        Extracts noun phrases from each document.
        Output: list of noun phrase strings.
        
        Inputs:
            nlp: spacy nlp object, usually initalized using 
                nlp = spacy.load('en')
            kwargs: dictionary corresponding to settings for this
                pipeline component. Currently unused.
    '''
    def __init__(self,nlp, kwargs):
        
        if not Doc.has_extension('easytext'):
            Doc.set_extension('easytext', default=dict())
            
    def __call__(self, doc):
        
        nounphrases = list()
        for nounphrase in doc.noun_chunks:
            #np_text = ' '.join(nounphrase)
            nounphrases.append(nounphrase.text.strip().lower())
        
        #doc._.easytext['nounphrasecounts'] = dict(Counter(nounphrases))
        doc._.easytext['nounphrases'] = nounphrases
        
        return doc

    
