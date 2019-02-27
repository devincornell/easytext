import sys
from glob import glob
import spacy
import pandas as pd
from argparse import ArgumentParser
import os.path
import re

from .easytext import easyparse
from .algorithms import glove, lda, nmf

#print(os.path.basename(your_path))

#from .easytext import EasyTextPipeline # (this one does it all)
#from .ner import ExtractEntsPipeline
#from .grammar import ExtractPrepositionsPipeline, ExtractNounVerbsPipeline, ExtractEntVerbsPipeline


from .tools import dict2df

def read_text_file(fname):
    with open(fname, 'rb') as f:
        text = f.read().decode('ascii',errors='ignore')
    return text



def make_parser():
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    parser = ArgumentParser()
    
    subparsers = parser.add_subparsers(dest='command')
    
    def add_to_subparser(subparser):
        subparser.add_argument('infiles', nargs='+', help='Input files.')
        subparser.add_argument('outfile', help='Output file.')
        
        subparser.add_argument('-dn','--doclabelcol', type=str, required=False, help='Column name for document title/id.')
        subparser.add_argument('-c','--textcol', type=str, default='text', help='Column name of text data (if excel file provided).')
        
        subparser.add_argument('-nhd','--nohdfonfail', action='store_true', help='Don\'t write hdf if the data is too big for excel.')
        
    
    # create the parser for topic modeling arguments
    tmparser = subparsers.add_parser('topicmodel', help='Run topic modeling algorithms (LDA or NMF).')
    add_to_subparser(tmparser)
    tmparser.add_argument('-n', '--numtopics', type=int, required=True, help='Numer of topics.')
    tmparser.add_argument('-t','--type', type=str, default='lda', help="From ('lda','nmf') choose algorithm.")
    tmparser.add_argument('-s','--seed', type=int, default=0, help='Seed to be used to init topic model.')
    tmparser.add_argument('-m','--min_tf', type=int, default=0, help='Seed to be used to init topic model.')
    tmparser.add_argument('-nswm','--nosave_wordmatrix', action='store_true', help='Don\'t save word matrix in excel (helps to make smaller files).')
    
    # create parser for glove
    gparser = subparsers.add_parser('glove', help='Run glove algorithm.')
    add_to_subparser(gparser)
    gparser.add_argument('-d', '--dimensions', type=int, required=True, help='Numer of embedding dimensions.')
    gparser.add_argument('-kw','--keywords', type=str, help='Keywords orient embedding dimensions.')
    gparser.add_argument('-s','--seed', type=int, default=0, help='Integer to see glove model estimation.')
    gparser.add_argument('-m','--min_tf', type=int, default=0, help='Seed to be used to init topic model.')
    gparser.add_argument('-nswm','--nosave_wordmatrix', action='store_true', help='Don\'t save word matrix in excel (helps to make smaller files).')
    
    # parser for entity extraction
    eparser = subparsers.add_parser('entities', help='Run Named Entity Recognition (NER).')
    add_to_subparser(eparser)
    eparser.add_argument('-v','--entverbs', action='store_true', help='T/F include entity-verb detection?')
    
    # parser for entity peace
    grparser = subparsers.add_parser('grammar', help='Run grammatical expression extraction.')
    add_to_subparser(grparser)
    grparser.add_argument('-v','--entverbs', action='store_true', help='T/F include entity-verb detection?')
    grparser.add_argument('-n','--nounverbs', action='store_true', help='T/F include noun-verb detection?')

    return parser



def filenames_to_docnames(fnames):
    '''
        Convert original file names to more readable names
            wile checking to make sure there are no collisions.
    '''
    newnames = list()
    for fn in fnames:
        base = os.path.basename(fn)
        basename = os.path.splitext(base)[0]
        newnames.append(basename)
    
    # check and make sure it didn't wipe out any redundancies
    # (this could happen if pulling from multiple folders or catching multiple file extensions)
    if len(set(newnames)) != len(newnames):
        newnames = fnames
    
    return newnames
        



def read_input_files(infiles,doclabelcol,textcol):
    '''
        Reads single or multiple text files or an excel/csv file.
    '''
    
    # read multiple text files
    if len(infiles) > 1:
        texts = [read_text_file(fn) for fn in infiles]
        docnames = filenames_to_docnames(infiles)
    
    else:
        fname = infiles[0]
        fext = os.path.splitext(os.path.basename(fname))[1]
        
        # read single text file
        if fext == '.txt':
            text = read_text_file(fname)
            textnames = [(i,t) for i,t in enumerate(text.split('\n')) if len(t) > 0]
            docnames = [str(i) for i,t in textnames]
            texts = [t for i,t in textnames]
            
        # read spreadsheet file using pandas
        elif fext in ('.xlsx','.xls','.csv',):
            try:
                if fext == '.csv':
                    df = pd.read_csv(fname)
                elif fext in ('.xlsx','.xls'):
                    df = pd.read_excel(fname)
            except:
                raise Exception('There was a problem reading the {} file.'.format(fext))
                
            # perform checks on column names
            if textcol not in df.columns:
                raise Exception('The text column name was not found in spreadsheet:', textcol)
            if doclabelcol is not None and doclabelcol not in df.columns:
                raise Exception('The column name for document labels was not found in the spreadsheet:', doclabelcol)
                
            # extract texts and doclabels
            texts = [str(v) for v in df[textcol]]
            if doclabelcol is not None:
                docnames = [str(n) for n in df[doclabelcol]]
            else:
                docnames = [str(i) for i in range(df.shape[0])]

        else:
            raise Exception('You need to pass an xls or 1+ txt files.')
            
    return texts, docnames


def parse_keywords(kw):
    if kw is None:
        return None
     
    kwgroups = [[w.strip() for w in kwg.split(',') if len(w.strip())>0] for kwg in kw.split('|')]
    kwgroups = [kwg for kwg in kwgroups if len(kwg)>0]
    
    return kwgroups
    
    
    



if __name__ == '__main__':
    
    # parse input according to defined parser
    parser = make_parser()
    args = parser.parse_args()
    
    # get parsed documents
    texts, docnames = read_input_files(args.infiles, args.doclabelcol, args.textcol)
    
    # check doclabelcols and texts
    assert(len(docnames) > 0 and len(docnames) == len(texts))
    assert(isinstance(texts[0],str) and isinstance(docnames[0],str))
    print(len(texts), 'texts identified.')
    
    
    # IMPLEMENT COMMAND FUNCTIONALITY
    nlp = spacy.load('en')
    if args.command == 'topicmodel':
        assert(args.numtopics > 0)
        assert(args.type.lower() in ('lda','nmf'))
        assert(args.numtopics < len(texts))
        
        print('converting', len(texts), 'texts to bags-of-words')
        bows = list()
        for pw in easyparse(nlp,texts,enable=['wordlist',]):
            if len(pw['wordlist']) > 0:
                bows.append(pw['wordlist'])
        
        print('performing topic modeling with', args.numtopics, 'topics.')
        tmfunc = nmf if args.type.lower() == 'nmf' else lda
        model = tmfunc(
            docbows=bows, 
            n_topics=args.numtopics, 
            docnames=docnames,
            min_tf=args.min_tf,
        )
        
        print('writing output report')
        final_fname = model.write_report(
            args.outfile, 
            save_wordmatrix=not args.nosave_wordmatrix, 
            featurename='topic',
            hdf_if_fail = not args.nohdfonfail,
        )
        print('saved result as', final_fname)
        
    elif args.command == 'glove':
        assert(args.dimensions > 0)
        assert(args.dimensions < len(texts))
        keywords = parse_keywords(args.keywords)
        
        # parse texts using spacy
        print('converting', len(texts), 'texts to sentence lists')
        docsents = list()
        for pw in easyparse(nlp,texts,enable=['sentlist']):
            if len(pw['sentlist']) > 0:
                docsents.append(pw['sentlist'])
        
        print('running glove algorithm with n =', args.dimensions)
        model = glove(
            docsents, 
            args.dimensions,
            docnames=docnames,
            keywords=keywords,
            min_tf=args.min_tf,
        )
        
        print('writing output report to', args.outfile)
        final_fname = model.write_report(
            args.outfile, 
            save_wordmatrix= not args.nosave_wordmatrix, 
            featurename='dimension',
            hdf_if_fail = not args.nohdfonfail,
        )
        print('saved result as', final_fname)
    
    elif args.command == 'entities':
        pass
    elif args.command == 'grammar':
        pass
    else:
        # note: parser gaurantees that one of these options would be set
        raise Exception('Weird error - the command {} hasn\'t been implemented.'.format(args.command))
    

    exit()
    #====================================================
        
    
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
    
        
        