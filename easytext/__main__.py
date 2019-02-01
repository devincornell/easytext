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
    with open(fname, 'r') as f:
        text = f.read()
    return text

if __name__ == '__main__':
    
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    parser = ArgumentParser()
    
    h = 'Run all modules.'
    parser.add_argument('--all', help=h, action='store_true')
    #parser.add_argument('-a', help=h, action='store_true')
    
    h = 'Run NER.'
    parser.add_argument('--entity', help=h, action='store_true')
    #parser.add_argument('-e', help=h, action='store_true')
    
    h = 'Run prepositional phrase extractor.'
    parser.add_argument('--preposition', help=h, action='store_true')
    #parser.add_argument('-p', help=h, action='store_true')
    
    h = 'Run noun-verb extractor.'
    parser.add_argument('--noun-verb', help=h, nargs='?')
    #parser.add_argument('-n', help=h, action='store_true')
    
    h = 'Run entity-verb extractor.'
    parser.add_argument('--entity-verb', help=h, action='store_true')
    #parser.add_argument('-v', help=h, action='store_true')
    
    args = parser.parse_args()
    print(args)
    exit()
    
    
    
    inoutfiles = [a for a in sys.argv[1:] if not a.startswith('-')]
    fullargs = [a[2:] for a in sys.argv[1:] if a.startswith('--')]
    charargs = [a[1:] for a in sys.argv[1:] if a.startswith('-') and not a.startswith('--')]
    
    
    # initial checks on arguments
    if len(inoutfiles) != 2:
        raise Exception('Command must include input and output file arguments.')
    
    if any([len(ca) > 1 for ca in charargs]):
        raise Exception('Character args start with a single "-" and full args start with "--".')
        
    if len(fullargs) + len(charargs) == 0:
        raise Exception('No actions were specified via arguments. Use --all flag to run all actions.')
    
    # define available options/flags
    infnames, outfname = inoutfiles
    flagstr = (
        ('a','all'),
        ('e','entity'),
        ('p','preposition'),
        ('n','noun-verb'),
        ('v','entity-verb'),
        ('s','sentiment'),
        ('t','topicmodel'),
    )
    
    # make sure all arguments are recognized
    allchr, allfull = [c for c,f in flagstr], [f for c,f in flagstr]
    for ca in charargs:
        if ca not in allchr:
            raise Exception('Character argument "', ca, '" not recognized.')
    for fa in fullargs:
        if fa not in allfull:
            raise Exception('Full argument "', fa, '" not recognized.')
    
    # combine flags into a dictionary
    flags = {f: c in charargs or f in fullargs for c,f in flagstr}
    print('Selected Flags:', flags)
        
    # load in text data
    if '*' in infnames:
        fnames = glob(infnames, recursive=True)
        if not len(fnames):
            raise Exception('Provided input pattern didn\'t match any filenames.')
        
        texts = (readfile(fn) for fn in fnames)
        names = fnames
    else:
        # every line is a separate text
        text = readfile(infnames)
        textnames = [(str(i),t) for i,t in enumerate(text.split('\n')) if len(t.strip()) > 0]
        
        names = [n for n,t in textnames]
        texts = [t for n,t in textnames] # this looks weird bc lines should be reflected in fname
        
        
    # load correct pipeline components
    nlp = spacy.load('en')
    if flags['all'] or flags['entity'] or flags['entity-verb']:
        p = ExtractEntsPipeline()
        nlp.add_pipe(p, last=True)
    
    if flags['all'] or flags['preposition']:
        p = ExtractPrepositionsPipeline()
        nlp.add_pipe(p, last=True)
        
    if flags['all'] or flags['noun-verb']:
        p = ExtractNounVerbsPipeline()
        nlp.add_pipe(p, last=True)
        
    if flags['all'] or flags['entity-verb']:
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
    xlswriter = pd.ExcelWriter(outfname)
    
    if len(entcts) > 0:
        entdf = dict2df(entcts, names)
        entdf.to_excel(xlswriter, sheet_name='Entities')
        
    if len(prepcts) > 0:
        prepdf = dict2df(prepcts, names)
        prepdf.to_excel(xlswriter, sheet_name='Prepositions')
        
    if len(nvcts) > 0:
        nvdf = dict2df(nvcts, names)
        vals = pd.Series(nvdf.index.get_level_values('value'))
        nvdf['nouns'] = list(vals.apply(lambda x: x[0]))
        nvdf['verbs'] = list(vals.apply(lambda x: x[1]))
        nvdf = nvdf[['nouns','verbs','count']]
        nvdf.index = nvdf.index.droplevel('value')
        nvdf.to_excel(xlswriter, sheet_name='NounVerbs')
        
    if len(evcts) > 0:
        evdf = dict2df(evcts, names)
        vals = pd.Series(evdf.index.get_level_values('value'))
        evdf['entities'] = list(vals.apply(lambda x: x[0]))
        evdf['verbs'] = list(vals.apply(lambda x: x[1]))
        evdf = evdf[['entities','verbs','count']]
        evdf.index = evdf.index.droplevel('value')
        evdf.to_excel(xlswriter, sheet_name='EntityVerbs')
        
    xlswriter.save()
    
    # load spacy with correct modules
    #usemodules = set()
    #if flags['all'] or flags['entity'] or flags['entity-verb']:
    #    usemodules.add('ner')
        
    #if flags['all'] or flags['entity-verb'] or flags['preposition'] or flags['noun-verb']:
    #    # enable parser/tagger
    #    usemodules &= {'tagger', 'parser'}
    
    #defaultmod = {'tagger', 'parser', 'ner'}
    #disablemodules = defaultmod - usemodules
    #nlp = spacy.load('en', disable=disablemodules)
    
    
    exit()
    # parse documents for processing
    docs = nlp.pipe(texts)
    
        
    # apply selected stages
    if flags['all'] or flags['entity']:
        entcts, totcts = get_ents(docs)
        df = dict2df(entcts,names)
        print(df)
    
    
                 
    # parse text file where every line is a separate doc
    allscores = list()
    for n,doc in texts:
        if doc:
            score = dic.score(doc)
            print('text on line', n+1, 'counts (', sum(score.values()), 'moral words):')
            for cat in dic.allcats:
                print('    ' + cat+':', score[cat])
            
            allscores.append(score)
    
    nlp.pipe(texts)
    
    score = addscores(allscores)
    print('total counts (', sum(score.values()), 'moral words total):')
    for cat in dic.allcats:
        print('    ' + cat+':', score[cat])
        
        
        
        