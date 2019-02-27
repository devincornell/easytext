

'''
    This file simply dumps the newsgroups 20 dataset from sklearn into the tmp/ folder for testing commands.


'''



from sklearn.datasets import fetch_20newsgroups
import sys
import os
import glob

if __name__ == '__main__':
    TARGET_DIR = 'tmp'
    
    # make dir if it doesn't exist
    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)
        print('Created new dir', TARGET_DIR)
    
    # delete .txt files if they already exist
    files = glob.glob(TARGET_DIR + '/' + '*.txt')
    i = 0
    for fname in files:
        os.remove(fname)
        i += 1
    print('Removed', i, 'files that previously existed.')
    
    if len(sys.argv) > 1:
        useN = int(sys.argv[1])
    else:
        useN = 100
    
    nd = fetch_20newsgroups(shuffle=True, random_state=0)
    texts, fnames =  nd['data'][:useN], nd['filenames'][:useN]

    for fn,t in zip(fnames,texts):
        with open(TARGET_DIR + '/'+fn.split('/')[-1]+'.txt', 'w') as f:
            f.write(t)
            
    print('Added', len(texts), 'new files to', TARGET_DIR)


