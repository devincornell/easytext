from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np
from collections import Counter
from glove import Glove, Corpus

from .glovetools import glove_transform_paragraph, glove_projection, supervised_vectors
from .docmodel import DocModel



def lda(docbows, n_topics, random_state=0, min_tf=2, learning_method='online', docnames=None, **kwargs):
    '''
        Interface for Latent Dirichlet Allocation algorithm using sklearn CountVectorizer and
            LatentDirichletAllocation methods.
            
        Output: Returns DocModel object containing the results of the topic model.
        
        Inputs: 
            docbows: Iterable of document token iterables
            n_topics: Number of documents to use in the topic model.
            random_state: Integer for seeding random generator. Allows
                for making reproducable topic models.
            min_tf: Minimum number of times a token must appear in 
                the corpus to be added to the topic model.
            learning_method: 'online' or 'batch', fed directly into the 
                sklearn LatentDirichletAllocation function.
            docnames: document names that will appear in DocModel
                for convenience.
            **kwargs: other keyword arguments fed directly into the 
                sklearn LatentDirichletAllocation function.
    '''
    
    vectorizer = CountVectorizer(tokenizer = lambda x: x, preprocessor=lambda x:x,min_df=min_tf)
    corpus = vectorizer.fit_transform(docbows)
    vocab = vectorizer.get_feature_names()
    
    lda_model = LatentDirichletAllocation(
        n_components=n_topics, 
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
    '''
        Interface for Non-negative Matrix Factorization algorithm using sklearn 
            TfidfVectorizer and NMF methods.
            
        Output: Returns DocModel object containing the results of the topic model.
        
        Inputs: 
            docbows: Iterable of document token iterables
            n_topics: Number of documents to use in the topic model.
            random_state: Integer for seeding random generator. Allows
                for making reproducable topic models.
            min_tf: Minimum number of times a token must appear in 
                the corpus to be added to the topic model.
            docnames: document names that will appear in DocModel
                for convenience.
            **kwargs: other keyword arguments fed directly into the 
                sklearn NMF function.
    '''
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


def calc_cutoffind(freqs,min_tf):
    '''
        Using an ordered frequency list (biggest->smallest), identifies index of 
            first item to be cut off.
        
        freqs: ordered frequency list (biggest->smallest)
        min_tf: smallest frequency to accept.
    '''
    if min_tf > freqs[0]:
        raise Exception('Cutoff {} is larger than largest frequency {}.'.format(min_tf,freqs[0]))
    if min_tf <= freqs[-1]:
        return len(freqs)
    
    i = 0
    while freqs[i] >= min_tf:
        i += 1
    
    return i
    
        
        
def glove(docsents, n_dim, random_state=0, min_tf=1, docnames=None, keywords=None, **kwargs):
    
    '''
        Interface for Glove algorithm using python-glove package.
            
        Output: Returns DocModel object containing the results of the word embedding.
        
        Inputs: 
            docbows: Iterable of document token iterables (nested by document, will 
                be flattened).
            n_dim: Number of dimensions to use in the embedding model.
            random_state: Integer for seeding random generator. Allows
                for making reproducable embedding models.
            min_tf: Minimum number of times a token must appear in 
                the corpus to be added to the topic model.
            docnames: document names that will appear in DocModel
                for convenience.
            keywords: list of lists of words that will form the basis of a 
                hyper-rotated version of a new embedding model. The list 
                [['hat','dog'],['cat',]] would orient the first (arbitrary)
                dimension of the vector space to hat + dog, and the second 
                to the vector for cat minus the component in hat + dog to 
                preserve orthogonality.
            **kwargs: other keyword arguments fed directly into the 
                sklearn NMF function.
    '''
    
    # count frequencies
    fdist = Counter([w for s in pretendsents(docsents) for w in s])
    sfdist = list(sorted(fdist.items(),key=lambda x:x[1],reverse=True))
    dictionary = {wf[0]:i for i,wf in enumerate(sfdist)}
    cutoff = calc_cutoffind([f for w,f in sfdist],min_tf)

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
    