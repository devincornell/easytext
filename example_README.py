
from example_data import get_testdata
from easytext import easyparse, lda, ALL_COMPONENTS
import spacy

if __name__ == '__main__':

    texts, docnames = get_testdata(10)
    texts # list of strings containing the texts of interest

    
    if False:
        # README.md FIRST EXAMPLE
        nlp = spacy.load('en')
        for etdoc in easyparse(nlp, texts, enable=['wordlist','entlist']):
            print(etdoc['wordlist'])
            print(etdoc['entlist'], end='\n\n')
            
    if True:
        # README.md SECOND EXAMPLE
        
        # preprocess documents into bags of words
        nlp = spacy.load('en')
        docbows = list()
        for etdoc in easyparse(nlp, texts, enable=['wordlist',]):
            docbows.append(etdoc['wordlist'])

        # create topic model
        topicmodel = lda(docbows, 10)

        # print topics most closely associated with each document
        print(topicmodel.doc_feature_summary(topn=5))
            
    if False:
        
        nlp = spacy.load('en')
        
        # loop through each component, one at a time, testing it out
        all_components = list(ALL_COMPONENTS.keys())
        for comp in all_components:
            print('\n\n', comp)
            for etdoc in easyparse(nlp, texts, [comp,],pipeargs=dict(use_ents=False,)):
                print(etdoc[comp][:3])
