from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np
from collections import Counter
from glove import Glove, Corpus

from .glovetools import glove_transform_paragraph, glove_projection, supervised_vectors
from .docmodel import DocModel

def lda(docbows, n_topics, random_state=0, min_tf=2, learning_method='online', docnames=None, **kwargs):

    vectorizer = CountVectorizer(tokenizer = lambda x: x, preprocessor=lambda x:x,min_df=min_tf)
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
    
    return DocModel(doctopics, topics, vocab, docnames=docnames)
    
def nmf(docbows, n_topics, random_state=0, min_tf=2, docnames=None, **kwargs):
    
    vectorizer = TfidfVectorizer(tokenizer = lambda x: x, preprocessor=lambda x:x,min_df=min_tf)
    corpus = vectorizer.fit_transform(docbows)
    vocab = vectorizer.get_feature_names()
    
    nmf_model = NMF(
        n_components=n_topics, 
        random_state=random_state,
        **kwargs,
       ).fit(corpus)
    
    doctopics = nmf_model.transform(corpus)
    topics = nmf_model.components_
    
    return DocModel(doctopics, topics, vocab, docnames=docnames)
    
def pretendsents(docsents):
    '''
        Shortcut to provide sentence list without copying to new variable
    '''
    for doc in docsents:
        for sent in doc:
            yield sent

def pretenddocs(docsents):
    '''
        Shortcut to provide document list without copying to new variable.
    '''
    for doc in docsents:
        yield [w for sent in doc for w in sent]



def glove(docsents, n_dim, random_state=0, min_tf=1, docnames=None, keywords=None, **kwargs):
    
    # count frequencies
    fdist = Counter([w for s in pretendsents(docsents) for w in s])
    sfdist = list(sorted(fdist.items(),key=lambda x:x[1],reverse=True))
    dictionary = {wf[0]:i for i,wf in enumerate(sfdist)}
    try:
        cutoff = [f for w,f in sfdist].index(min_tf)
    except ValueError:
        cutoff = len(sfdist)

    # calculate corpus matrix
    corpus = Corpus(dictionary=dictionary)
    corpus.fit(pretendsents(docsents), window=10) # GloVe found that bigger windows helped
    corpus.matrix = corpus.matrix.tocsr()[:cutoff,:cutoff].tocoo()
    
    # train glove model
    glove = Glove(no_components=n_dim, learning_rate=0.05, random_state=random_state)
    glove.fit(corpus.matrix, **kwargs)
    
    # modify dictionary after cutoff applied
    cutoff_dictionary = {wf[0]:i for i,wf in enumerate(sfdist) if wf[1]>min_tf}
    glove.add_dictionary(cutoff_dictionary)
    vocab = [w for w,f in sfdist if f > min_tf]
    
    # if keywords provided, transform vector space to new basis based on keywords
    if keywords is not None:
        glove = supervised_vectors(glove, keywords)
    
    # transform documents to single vectors
    transpar = lambda doc: glove_transform_paragraph(glove, doc,ignore_missing=True)
    docvectors = [transpar(doc) for doc in pretenddocs(docsents)]
    
    # words associated with each dimension of the embedding space
    dimwords = np.zeros((n_dim,len(vocab)))
    for dim in range(n_dim):
        # create natural basis unit vector
        e = np.zeros(n_dim)
        e[dim] = 1
        for i,w in enumerate(vocab):
            dimwords[dim,i] = glove_projection(glove, w, e)
    
    return DocModel(np.vstack(docvectors), dimwords, vocab, docnames=docnames)
    