
from glob import glob
from argparse import ArgumentParser

from .fileio import read_input_files

# store all subcommands
from .subcommand_functions import *
all_subcommands = {
    'wordcount':{'argparser':subcommand_wordcount_args, 'command':subcommand_wordcount},
    'sentiment':{'argparser':subcommand_sentiment_args, 'command':subcommand_sentiment},
    'entities':{'argparser':subcommand_entities_args, 'command':subcommand_entities},
    'topicmodel':{'argparser':subcommand_topicmodel_args, 'command':subcommand_topicmodel},
    'glove':{'argparser':subcommand_glove_args, 'command':subcommand_glove},
    'grammar':{'argparser':subcommand_grammar_args, 'command':subcommand_grammar},
}



def make_parser(subcommands):
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    main_parser = ArgumentParser()
    
    main_subparsers = main_parser.add_subparsers(dest='command')
    main_subparsers.required = True
    
    # add all subcommands to parser
    for command,funcs in subcommands.items():
        funcs['argparser'](main_parser,main_subparsers)

    return main_parser






if __name__ == '__main__':
    
    # parse input according to defined parser
    #parser = make_parser()
    parser = make_parser(all_subcommands)
    args = parser.parse_args()
    
    # get parsed documents
    texts, docnames = read_input_files(args.infiles, args.doclabelcol, args.textcol)
    
    # check doclabelcols and texts
    assert(len(docnames) > 0 and len(docnames) == len(texts))
    assert(isinstance(texts[0],str) and isinstance(docnames[0],str))
    print(len(texts), 'texts identified.')
    
    
    # COMMAND FUNCTIONALITY MOSTLY IN subcommand_functions file
    if args.command not in all_subcommands.keys():
        # parser should handle invalid commands, but just in case.
        raise Exception('Your subcommand was not recognized!')
        
        
    # envoke the appropriate subcommand functions
    final_fname = all_subcommands[args.command]['command'](texts, docnames, args)
    print('saved', args.command, 'result as', final_fname)


    
        
        