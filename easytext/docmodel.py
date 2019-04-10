import pandas as pd
import os.path


from .reports import write_report

class DocModel:
    '''
        This class contains a representation of documents in a corpus according
            to some number of dimensions.
        It is currently being used for LDA and NMF topic models and Glove
            document representations.
    '''
    def __init__(self, doc_features, feature_words, vocab, docnames=None, model=None):
        
        '''
            Represents Nd documents according to Nf features which are composed
                of Nt tokens (or an arbitrary basis set).
                
            Inputs:
                doc_features: <Nd x Nf> matrix of document representations.
                    (i.e. topic distributions, embedding vectors, etc)
                feature_words: <Nf x Nt> matrix of feature representations
                    in terms of tokens (or some arbitrary basis more generally).
                vocab: actual tokens that compose the Nt basis dimensions
                docnames: a convenient input of document names that will be 
                    return in class methods.
                model: arbitrary object for storing original sklearn LDA, NMF
                    or glove models with associated training parameters.
        '''
        
        # doc_features is <Ndocs X Nfeat> and feature_words is <Nvocab X Nvocab>
        assert(doc_features.shape[1] == feature_words.shape[0])
        assert(len(vocab) == feature_words.shape[1])
        
        self.Ndocs = doc_features.shape[0]
        self.Nfeat = doc_features.shape[1]
        self.Nvocab = feature_words.shape[1]
        
        # optional data for storage
        self.vocab = vocab
        self.model = model
        
        # name documents as integers if not docnames provided
        self.docnames = docnames if docnames is not None else list(range(self.Ndocs))        
        
        # features are topics or dimensions in the embedding space
        self.doc_features = pd.DataFrame(doc_features,index=self.docnames)
        self.doc_features.index.name = 'document'
        self.doc_features.columns.name = 'feature'
        
        self.feature_words = pd.DataFrame(feature_words,columns=vocab)
        self.feature_words.index.name = 'feature'
        self.feature_words.columns.name = 'word'
        
        
    def set_docnames(self,newdocnames):
        self.doc_features.index = newdocnames
        self.docnames = newdocnames
        
    def get_feature_docs(self, feature, topn=None):
        '''
            Gives documents most closely associated with a given feature.
            Input:
                feature: number corresponding to the desired feature.
                topn: number of document ids to return.
        '''
        assert(feature >= 0 and feature < self.Nfeat)
        
        # series specifying values for each document along the particular feature
        topdocs = self.doc_features.loc[feature].sort_values(ascending=False)
        return topdocs[:topn]
    
    def get_feature_words(self, feature, topn=None):
        '''
            Gives words most closely associated with a given feature.
            Input:
                feature: number corresponding to the desired feature.
                topn: number of document ids to return.
        '''
        assert(feature >= 0 and feature < self.Nfeat)
        
        topwords = self.feature_words.loc[feature,:].sort_values(ascending=False)
        return topwords[:topn]
    
    def get_doc_features(self, doc, topn=None):
        '''
            Gives features most closely associated with a given doc.
            Input:
                doc: document id assigned through the constructure 
                    'docnames' parameter or index of document.
                topn: number of feature ids to return.
        '''
        assert(doc in self.docnames)
        
        # series specifying values for each document along the particular feature
        topfeat = self.doc_features.loc[doc,:].sort_values(ascending=False)
        return topfeat[:topn]
        
    def get_word_features(self, word, topn=None):
        '''
            Gives features most closely associated with a given word.
            Input:
                word: word (or arbitrary basis name) to get features of.
                topn: number of feature ids to return.
        '''
        assert(word in self.feature_words.columns)
        
        # series specifying values for each document along the particular feature
        topfeat = self.feature_words.loc[:,word].sort_values(ascending=False)
        return topfeat[:topn]
    
    
    # ________ Create Summary DataFrames _________
    def feature_words_summary(self,topn=None):
        '''
            Shows words most closely associated with each feature.
            Input:
                topn: number of words to return.
        '''
        if topn is None:
            topn = len(self.vocab)
        
        df = pd.DataFrame(index=range(self.Nfeat),columns=range(topn))
        df.index.name = 'feature'
        df.columns.name = 'nth top word'
        for feat in range(self.Nfeat):
            topwords = self.get_feature_words(feat, topn)
            df.loc[feat,:] = list(topwords.index)
        
        return df
            
    def doc_feature_summary(self, topn=None):
        '''
            Shows features most closely associated with each document.
            Input:
                topn: number of features to return.
        '''
        
        if topn is None:
            topn = self.Nfeat
        
        useNfeat = min(topn, self.Nfeat)
        df = pd.DataFrame(index=self.docnames, columns=range(useNfeat))
        df.index.name = 'document'
        df.columns.name = 'nth top feature'
        for doc in self.docnames:
            topfeat = self.get_doc_features(doc, useNfeat)
            df.loc[doc,:] = list(topfeat.index)
        
        return df
    
    def write_report(self, fname, save_wordmatrix=False, featurename=None, summary_topn=None, **kwargs):
        '''
            simply calls write_report after inputting desired dataframes.
            inputs:
                fname: file destination.
                save_wordmatrix: T/F save word matrix to output. This 
                    file can be huge, so may not always be able to do 
                    it.
                featurename: name of feature for sheet titles. For a topic
                    model, should be 'topic'. For embedding model, should 
                    be 'dimension'.
                summary_topn: number of words/features to return in the 
                    summary pages.
                **kwargs goes to write_report() directly.
        '''
        if featurename is None:
            featurename = 'feature'
            
        sheets = list()
        sheets.append(('doc_{}'.format(featurename),self.doc_features))
        if save_wordmatrix: sheets.append(('{}_words'.format(featurename), self.feature_words))
        sheets.append(('doc_summary', self.doc_feature_summary(summary_topn)))
        sheets.append(('{}_summary'.format(featurename),self.feature_words_summary(summary_topn)))
        
        return write_report(fname, sheets, **kwargs)
    

        

    

        