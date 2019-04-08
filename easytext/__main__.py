
from glob import glob
from argparse import ArgumentParser

from .fileio import read_input_files
from .subcommand_functions import *


def make_parser():
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    parser = ArgumentParser()
    
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    
    def add_to_subparser(subparser):
        subparser.add_argument('infiles', nargs='+', help='Input files.')
        subparser.add_argument('outfile', help='Output file.')
        
        subparser.add_argument('-dn','--doclabelcol', type=str, required=False, help='Column name for document title/id.')
        subparser.add_argument('-c','--textcol', type=str, default='text', help='Column name of text data (if excel file provided).')
        
        subparser.add_argument('-nhd','--nohdfonfail', action='store_true', help='Don\'t write hdf if the data is too big for excel.')
    
    # create the parser for word counts
    wparser = subparsers.add_parser('wordcount', help='Word count across corpus, either by (a) manually selecting words to count or (b) selecting a minimum frequency of words to count.')
    add_to_subparser(wparser)
    wparser.add_argument('-w','--words', type=str, help='Comma-separated words to count in each document. Each word will be a column. i.e. "word1,word2" to count just two words.')
    wparser.add_argument('-m','--min_tf', type=int, default=1, help='Count all words that appear a minimum of min_tf times in corpus. Warning: could lead to really large & sparse output files.')
    wparser.add_argument('-hr','--human-readable', action='store_true', help='Organize output to be read by humans.')
    
    # parser for sentiment analysis
    sparser = subparsers.add_parser('sentiment', help='Compute sentiment analysis on corpus using Stanford empath.')
    add_to_subparser(sparser)
    sparser.add_argument('-o','--posneg-only', action='store_true', help='Include only positive and negative emotion categories.')
    sparser.add_argument('-n','--no-normalize', action='store_true', help='Don\'t normalize counts by document length.')
    sparser.add_argument('-hr','--human-readable', action='store_true', help='Organize output to be read by humans.')
    
    
    # parser for entity extraction
    eparser = subparsers.add_parser('entities', help='Run Spacy Named Entity Recognition (NER).')
    add_to_subparser(eparser)
    eparser.add_argument('-m','--min_tf', type=int, default=1, help='Minimum number of total entity occurrences to include in the model.')
    eparser.add_argument('-hr','--human-readable', action='store_true', help='Organize output to be read by humans.')
    eparser.add_argument('-ut','--use-types', type=str, help='Entity types to use. Format: "etype1,etype2".')
    eparser.add_argument('-it','--ignore-types', type=str, help='Entity types to ignore. Format: "etype1,etype2".')
    
    
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
    gparser.add_argument('-kw','--keywords', type=str, help='Keywords orient embedding dimensions. Format: "word1,word2|word3", where vector dimension 1 is "word1" + "word2", and dimension 2 is the vector "word3" rejected from dimension 1.')
    gparser.add_argument('-m','--min_tf', type=int, default=0, help='Minimum number of word occurrences to include in the model.')
    gparser.add_argument('-nswm','--nosave_wordmatrix', action='store_true', help='Don\'t save word matrix in excel (helps to make smaller files).')
    
    # parser for entity peace
    grparser = subparsers.add_parser('grammar', help='Run grammatical expression extraction.')
    add_to_subparser(grparser)
    grparser.add_argument('-v','--entverbs', action='store_true', help='T/F include entity-verb detection?')
    grparser.add_argument('-n','--nounverbs', action='store_true', help='T/F include noun-verb detection?')

    return parser



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
    
    
    # COMMAND FUNCTIONALITY MOSTLY IN subcommand_functions file
    nlp = spacy.load('en')
    
    if args.command == 'wordcount':
        final_name = subcommand_wordcount(texts, docnames, args)
        print('saved wordcount result as', final_fname)
        
    elif args.command == 'sentiment':
        final_name = subcommand_sentiment(texts, docnames, args)
        print('saved wordcount result as', final_fname)
    
    elif args.command == 'entities':
        final_name = subcommand_entities(texts, docnames, args)
        print('saved result as', final_fname)
        
    elif args.command == 'topicmodel':
        final_name = subcommand_topicmodel(texts, docnames, args)
        print('saved result as', final_fname)
        
    elif args.command == 'glove':
        final_name = subcommand_glove(texts, docnames, args)
        print('saved result as', final_fname)

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
    
        
        