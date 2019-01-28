import sys
from glob import glob
from dictcounter import DictCounter, addscores

def readfile(fname):
    with open(fname, 'r') as f:
        text = f.read()
    return text


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception('You need to pass exactly two arguments: python -m dictcounter <dict_file> <text_file>')
    
    dict_fname = sys.argv[1]
    text_fname = sys.argv[2]
    
    dic = DictCounter(dict_fname)
    
    
    
    if '*' in text_fname:
        # every text file is a separate text
        fnames = glob(text_fname, recursive=True)
        if not len(fnames):
            raise Exception('Provided glob didn\'t match any filenames.')
        
        texts = [(fn,readfile(fn)) for fn in fnames]
    else:
        # every line is a separate text
        with open(text_fname, 'r') as f: text = f.read()
        texts = enumerate(text.split('\n'))
    
    # parse text file where every line is a separate doc
    
    allscores = list()
    for n,doc in texts:
        if doc:
            score = dic.score(doc)
            print('text on line', n+1, 'counts (', sum(score.values()), 'moral words):')
            for cat in dic.allcats:
                print('    ' + cat+':', score[cat])
            
            allscores.append(score)
    
    score = addscores(allscores)
    print('total counts (', sum(score.values()), 'moral words total):')
    for cat in dic.allcats:
        print('    ' + cat+':', score[cat])
        
        
        
        