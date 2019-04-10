from example_dumpnewsgroup20 import make_spreadsheet
import pandas as pd
from easytext import easyparse, ALL_COMPONENTS
import spacy

if __name__ == '__main__':
    # run command to make spreadsheet file for example
    fname = 'tmp_example.csv'
    useN = 100
    make_spreadsheet(useN, fname)
    
    # read in csv file
    df = pd.read_csv(fname)
    
    valid_components = list(ALL_COMPONENTS.keys())
    texts, docnames = list(df['text']), list(df['title'])
    
    nlp = spacy.load('en')
    for etdoc in easyparse(nlp, texts, enable=['entverbs',]):
        entverbs = etdoc['entverbs']
        if len(entverbs) > 0:
            print(entverbs[0])
    
    #print(df)