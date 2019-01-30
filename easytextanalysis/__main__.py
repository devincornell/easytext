import sys
from glob import glob
import spacy
from spacy.tokens import Doc

from .grammar import get_ents
from .tools import dict2df

def readfile(fname):
    with open(fname, 'r') as f:
        text = f.read()
    return text


if __name__ == '__main__':
    
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    
    
    inoutfiles = [a for a in sys.argv[1:] if not a.startswith('-')]
    fullargs = [a[2:] for a in sys.argv[1:] if a.startswith('--')]
    charargs = [a[1:] for a in sys.argv[1:] if a.startswith('-')]
    
    
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
        ('v','entity-verb'),
        ('p','preposition'),
        ('n','noun-verb'),
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
        texts = [(str(i),t) for i,t in enumerate(text.split('\n')) if len(t.strip()) > 0]
        
        texts = [t for n,t in texts] # this looks weird bc lines should be reflected in fname
        names = [n for n,t in texts]
    
    
    # load spacy with correct modules
    usemodules = set()
    if flags['all'] or flags['entity'] or flags['entity-verb']:
        usemodules.add('ner')
        
    if flags['all'] or flags['entity-verb'] or flags['preposition'] or flags['noun-verb']:
        # enable parser/tagger
        usemodules &= {'tagger', 'parser'}
    
    defaultmod = {'tagger', 'parser', 'ner'}
    disablemodules = defaultmod - usemodules
    nlp = spacy.load('en', disable=disablemodules)
    
    
    # parse documents for processing
    docs = nlp.pipe(texts)
    
        
    # apply selected stages
    if flags['all'] or flags['entity']:
        entcts, totcts = get_ents(docs)
        df = dict2df(entcts,names)
        print(df)
    
                 
                 
    exit()
    
                 
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
        
        
        
        