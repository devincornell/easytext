from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np

from .docmodel import DocModel

def lda(docbows, n_topics, random_state=0, learning_method='online', **kwargs):

    vectorizer = CountVectorizer(tokenizer = lambda x: x, preprocessor=lambda x:x)
    corpus = vectorizer.fit_transform(docbows)
    vocab = vectorizer.get_feature_names()
    
    lda_model = LatentDirichletAllocation(
        n_topics=n_topics, 
        learning_method=learning_method,
        random_state=random_state, 
        **kwargs,
       ).fit(corpus)
    
    doctopics = lda_model.transform(corpus)
    topics = lda_model.components_
    
    # NOTE: Normalizing accordign to this page:
    #https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html
    topics = topics/topics.sum(axis=1)[:, np.newaxis]
    
    return DocModel(doctopics, topics, vocab)
    
def nmf(docbows, n_topics, random_state=0, **kwargs):
    
    vectorizer = TfidfVectorizer(tokenizer = lambda x: x, preprocessor=lambda x:x)
    corpus = vectorizer.fit_transform(docbows)
    vocab = vectorizer.get_feature_names()
    
    nmf_model = NMF(
        n_components=n_topics, 
        random_state=random_state, 
        **kwargs,
       ).fit(corpus)
    
    doctopics = nmf_model.transform(corpus)
    topics = nmf_model.components_
    
    return DocModel(doctopics, topics, vocab)
    
def doc2vec(sents, n_dim, random_state=0):
    return None
    