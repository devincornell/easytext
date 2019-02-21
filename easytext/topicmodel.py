


    
'''
>>> from gensim.test.utils import common_texts
>>> from gensim.corpora.dictionary import Dictionary
>>>
>>> # Create a corpus from a list of texts
>>> common_dictionary = Dictionary(common_texts)
>>> common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
>>>
>>> # Train the model on the corpus.
>>> lda = LdaModel(common_corpus, num_topics=10)
'''
    
    

def lda(bowtexts, Nt, verbose=False, min_tf=2, seed=0, alpha=None, beta=None, max_iter=100, tau_0=10):
    #NOTE HAS NOT BEEN UPDATED SINCE CHANGING TOPICMODEL CLASS
    '''
        bowtexts: list of lists of words to be modeled.
        Nt: number of topics to find.
    '''
    if verbose:
        print(len(bowtexts), 'documents found with average of', statistics.mean([len(doc) for doc in bowtexts]), 'words each.')
    
    
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=min_tf, stop_words='english')
    tf = tf_vectorizer.fit_transform([' '.join(t) for t in bowtexts])
    tf_feature_names = tf_vectorizer.get_feature_names()
    
    # run transform
    lda = LatentDirichletAllocation(n_topics=Nt, max_iter=max_iter, learning_method='online', random_state=seed, doc_topic_prior=alpha, topic_word_prior=beta, learning_offset=tau_0).fit(tf)
    doctopics = lda.transform(tf)
    
    # build output object
    #topicmodel = TopicModel(lda, tf_feature_names, doctopics)
    
    print(doctopics)
    
    # display topics to user
    if verbose:
        topicmodel.print_topics(8)
        
    return topicmodel
