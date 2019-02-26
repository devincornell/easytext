import random
import string
import spacy
import easytext as et

from sklearn.datasets import fetch_20newsgroups

def get_newsdocs():
    nd = fetch_20newsgroups(shuffle=True, random_state=0)
    return nd['data'], nd['filenames']

def randstr(N=3):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    
    
if __name__ == '__main__':
    useN = 500
    texts, docnames = get_newsdocs()
    texts = texts[:useN]
    docnames = docnames[:useN]
    
    nlp = spacy.load('en', disable=['ner',])
    bows = list() # used for topic modeling
    docsents = list() # used for glove
    for pw in et.easyparse(nlp,texts,enable=['sentlist','wordlist']):
        bows.append(pw['wordlist'])
        docsents.append(pw['sentlist'])
    
    print('finished parsing documents')
    
    show_nwords = 30
    et.create_algorithm_spreadsheet('nmf', 'nmftest.xlsx', show_nwords, docbows=bows, n_topics=10, docnames=docnames)
    et.create_algorithm_spreadsheet('lda', 'ldatest.xlsx', show_nwords, docbows=bows, n_topics=10, docnames=docnames)
    keywords = (('sports','opposed','soldier'),('istanbul','chicago'))
    et.create_algorithm_spreadsheet('glove', 'glovetest.xlsx', show_nwords, docsents=docsents, n_dim=10, docnames=docnames, keywords=keywords)
    
    