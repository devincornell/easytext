
from glob import glob
from argparse import ArgumentParser

from .fileio import read_input_files
from .subcommand_functions import all_subcommands


def make_parser(subcommands):
    # example: python -m easytextanalysis --sentiment --topicmodel --prepphrases texts/* output.csv
    main_parser = ArgumentParser()
    
    main_subparsers = main_parser.add_subparsers(dest='command')
    main_subparsers.required = True
    
    # add all subcommands to parser
    for command,funcs in subcommands.items():
        funcs['argparser'](main_parser,main_subparsers)

    return main_parser



def parse_keywords(kw):
    if kw is None:
        return None
     
    kwgroups = [[w.strip() for w in kwg.split(',') if len(w.strip())>0] for kwg in kw.split('|')]
    kwgroups = [kwg for kwg in kwgroups if len(kwg)>0]
    
    return kwgroups


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


    
        
        