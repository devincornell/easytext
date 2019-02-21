import sys
from glob import glob
import spacy
from spacy.tokens import Doc
import pandas as pd
from argparse import ArgumentParser

#from .easytext import EasyTextPipeline # (this one does it all)
from .ner import ExtractEntsPipeline
from .grammar import ExtractPrepositionsPipeline, ExtractNounVerbsPipeline, ExtractEntVerbsPipeline


from .tools import dict2df

def readfile(fname):
    with open(fname, 'rb') as f:
        text = f.read().decode('ascii',errors='ignore')
    return text


if __name__ == '__main__':
    
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    parser = ArgumentParser()
    h = 'Run all modules.'
    parser.add_argument('-a','--all', help=h, action='store_true')
    h = 'Run Named Entity Recognition (NER).'
    parser.add_argument('-e','--entity', help=h, action='store_true')
    h = 'Run prepositional phrase extractor.'
    parser.add_argument('-p','--preposition', help=h, action='store_true')
    h = 'Run noun-verb extractor.'
    parser.add_argument('-n','--noun-verb', help=h, action='store_true')
    h = 'Run entity-verb extractor.'
    parser.add_argument('-v','--entity-verb', help=h, action='store_true')
    h = 'Input files.'
    parser.add_argument('infiles', nargs='+', help=h)
    h = 'Output file.'
    parser.add_argument('outfile', help=h)
    args = parser.parse_args()
    
    # read text files
    if len(args.infiles) > 1:
        #args.infiles = args.infiles[:2]
        texts = (readfile(fn) for fn in args.infiles)
        names = args.infiles
    else:
        text = readfile(args.infiles[0])
        textnames = [(i,t) for i,t in enumerate(text.split('\n')) if len(t) > 0]
        names = [str(i) for i,t in textnames]
        texts = [t for i,t in textnames]
        
        
    # load correct pipeline components
    nlp = spacy.load('en')
    if args.all or args.entity or args.entity_verb:
        p = ExtractEntsPipeline()
        nlp.add_pipe(p, last=True)
    
    if args.all or args.preposition:
        p = ExtractPrepositionsPipeline()
        nlp.add_pipe(p, last=True)
        
    if args.all or args.noun_verb:
        p = ExtractNounVerbsPipeline()
        nlp.add_pipe(p, last=True)
        
    if args.all or args.entity_verb:
        p = ExtractEntVerbsPipeline()
        nlp.add_pipe(p, last=True)
        
    pipecomp = [n for n,p in nlp.pipeline]

    entcts = list()
    prepcts = list()
    nvcts = list()
    evcts = list()
    for name, doc in zip(names, nlp.pipe(texts)):
        
        if 'entities' in pipecomp:
            entcts.append(doc._.entcts)
        
        if 'prepositions' in pipecomp:
            prepcts.append(doc._.prepphrasecounts)
        
        if 'nounverbs' in pipecomp:
            nvcts.append(doc._.nounverbcounts)
        
        if 'entverbs' in pipecomp:
            evcts.append(doc._.entverbcts)
        
        
    # attach spreadsheet components
    xlswriter = pd.ExcelWriter(args.outfile, engine='xlsxwriter')
    
    if len(entcts) > 0:
        entdf = dict2df(entcts, names)#.applymap(escape)
        entdf.to_excel(xlswriter, sheet_name='Entities')
        
    if len(prepcts) > 0:
        prepdf = dict2df(prepcts, names)#.applymap(escape)
        prepdf.to_excel(xlswriter, sheet_name='Prepositions')
        
    if len(nvcts) > 0:
        nvdf = dict2df(nvcts, names)#.applymap(escape)
        vals = pd.Series(nvdf.index.get_level_values('value'))
        nvdf['nouns'] = list(vals.apply(lambda x: x[0]))
        nvdf['verbs'] = list(vals.apply(lambda x: x[1]))
        nvdf = nvdf[['nouns','verbs','count']]
        nvdf.index = nvdf.index.droplevel('value')
        nvdf.to_excel(xlswriter, sheet_name='NounVerbs')
        
    if len(evcts) > 0:
        evdf = dict2df(evcts, names)#.applymap(escape)
        vals = pd.Series(evdf.index.get_level_values('value'))
        evdf['entities'] = list(vals.apply(lambda x: x[0]))
        evdf['verbs'] = list(vals.apply(lambda x: x[1]))
        evdf = evdf[['entities','verbs','count']]
        evdf.index = evdf.index.droplevel('value')
        evdf.to_excel(xlswriter, sheet_name='EntityVerbs')
        
    xlswriter.save()
    
        
        