
'''
    This script is used to test the algorithm code: nmf, lda, and glove.

'''

from examples.example_data import get_testdata
import easytext as et

#from subprocess import run
import os

if __name__ == '__main__':
    
    texts, docids = get_testdata(useN=100)
    
    nmf = et.nmf(texts, 5, docnames = docids, include_model=True)
    
    newtexts, newdocids = get_testdata(useN=100)
    
    doctopics = nmf.transform(newtexts)
    print(doctopics)