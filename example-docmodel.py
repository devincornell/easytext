
'''
    This script is used to test the algorithm code: nmf, lda, and glove.

'''

import easytext as et
import numpy as np

if __name__ == '__main__':
    
    X = np.random.rand(8,4)
    X[X<0.2] = np.nan
    Y = np.random.rand(4,6)
    
    dm = et.DocModel(X, Y)
    print(dm)
    
    print(dm.get_doc_features(0))
    print(dm.get_doc_features(0, sort=True, topn=5))
    
    print(dm.get_feature_docs(0))
    print(dm.get_feature_docs(0, sort=True, topn=5))
    
    print(dm.get_feature_basis(0))
    print(dm.get_feature_basis(0, sort=True, topn=5))
    
    print(dm.get_doc_summary(topn=3))
    print(dm.get_doc_summary(topn=3, human=True))
    
    print(dm.get_feature_doc_summary(topn=3))
    print(dm.get_feature_doc_summary(topn=3, human=True))
    
    print(dm.get_feature_summary(topn=3))
    print(dm.get_feature_summary(topn=3, human=True))
    