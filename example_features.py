import random
import string
import easytext as et

def randstr(N=3):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def getdocs():
    toksiz = 3
    vocsiz = 100
    Ndocs = 1000
    docsiz = 100
    vocab = [randstr(toksiz) for _ in range(vocsiz)]
    bows = [random.choices(vocab,k=docsiz) for _ in range(Ndocs)]
    return bows
    
    
if __name__ == '__main__':
    
    bows = getdocs()
    
    tm = et.nmf(bows,10)
    
    #print('get_feature_docs')
    #print(tm.get_feature_docs(0,topn=5))
    
    print('get words closest to each feature')
    print(tm.feature_words_summary(topn=5))
    
    print(tm.doc_feature_summary(topn=5))
    
    
    