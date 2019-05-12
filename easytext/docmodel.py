import pandas as pd
import os.path
import spacy
from scipy.sparse import csr_matrix

from .reports import write_report

class DocModel:
    '''
        This class contains a representation of documents in a corpus according
            to some number of dimensions.
        It is currently being used for LDA and NMF topic models and Glove
            document representations.
    '''
    def __init__(self, doc_features, docnames=None, featnames=None, model=None, feature_words=None, vocab=None, vectorizer=None, df_type=pd.SparseDataFrame):
        
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
        
        # convert doc_features to dataframe
        if isinstance(doc_features, pd.DataFrame) or isinstance(doc_features, list):
            self.doc_feat = df_type(doc_features)
        
        else:
            # create dataframe with provided docnames and featnames
            self.doc_feat = df_type(doc_features)
            
            docrange = list(range(doc_features.shape[0]))
            docnames = list(docnames) if docnames is not None else docrange
            
            featrange = list(range(doc_features.shape[1]))
            featnames = list(featnames) if featnames is not None else featrange
            
            self.doc_feat.index = docnames
            self.doc_feat.columns = featnames
            
        # dimension sizes
        self.Ndocs = doc_features.shape[0]
        self.Nfeat = doc_features.shape[1]
        #self.Nbase = doc_features.shape[1]
        
        # doc_features is <Ndocs X Nfeat> and feature_words is <Nvocab X Nvocab>
        
        if feature_words is not None:
            assert(doc_features.shape[1] == feature_words.shape[0])
            assert(len(vocab) == feature_words.shape[1])
        
            self.feature_words = pd.DataFrame(feature_words,columns=vocab)
            self.feature_words.index.name = 'feature'
            self.feature_words.columns.name = 'word'
            self.Nvocab = feature_words.shape[1]
            self.vocab = vocab
        

        
        # optional data for storage
        self.model = model
        self.vectorizer = vectorizer
        
        # name documents as integers if not docnames provided
        self.docnames = docnames if docnames is not None else list(range(self.Ndocs))
        self.featnames = featnames if featnames is not None else list(range(self.Nfeat))
        
        # features are topics or dimensions in the embedding space
        self.doc_features = pd.DataFrame(doc_features,index=self.docnames, columns=self.featnames)
        self.doc_features.index.name = 'document'
        self.doc_features.columns.name = 'feature'
        

    def _has_feature_words():
        try:
            self.feature_words
            self.vocab
        except:
            raise Exception('feature_words and/or vocab were not provided in DocModel construcor!')
        
    
    # ________ Create Summary DataFrames _________
    def get_doc_features(self, doc, sort=False, topn=None):
        '''
            Gives features of a given goc. If sort, will 
                return features most closely associated with the doc.
            Input:
                doc: document id assigned through the constructure 
                    'docnames' parameter or index of document.
                sort: return feat most closely associated with 
                    the doc.
                topn: number of feature ids to return.
        '''
                
        assert(doc in self.doc_feat.index)
        if not sort:
            return self.doc_feat.loc[doc,:].to_dense()
        
        else:
            topfeat = self.doc_feat.loc[doc,:].sort_values(ascending=False)
            return topfeat[:topn].to_dense()
        
    def get_doc_summary(self, topn=None):
        '''
            Creates 
        '''
        if topn is None:
            cols = range(self.doc_feat.shape[1])
        else:
            cols = range(topn)
        
        df = pd.DataFrame(index=self.doc_feat.index, cols=cols)
        for doc in self.doc_feat.index:
            df.loc[doc,:] = self.get_doc_features(doc, sort=True, topn=topn)
        
        return df
        
        
    def get_feature_docs(self, feature, sort=False, topn=None):
        '''
            Gives documents most closely associated with a given feature.
            Input:
                feature: feature id to retrieve.
                topn: number of document ids to return.
        '''
        
        assert(feature in self.doc_feat.columns)
        if not sort:
            return self.doc_feat.loc[:,feature].to_dense()
        
        else:
            topdocs = self.doc_feat.loc[:,feature].sort_values(ascending=False)
            return topdocs[:topn].to_dense()
        

    def get_feature_summary(self, topn=None):
        '''
            Creates 
        '''
        if topn is None:
            cols = range(self.doc_feat.shape[0])
        else:
            cols = range(topn)
        
        df = pd.DataFrame(index=self.doc_feat.index, cols=cols)
        for feat in self.doc_feat.columns:
            df.loc[doc,:] = self.get_doc_features(doc, sort=True, topn=topn)
        
        return df
        
        
        
    # ________ Create Summary DataFrames _________
    def feature_words_summary(self, topn=None):
        '''
            Shows words most closely associated with each feature.
            Input:
                topn: number of words to return.
        '''
        self._has_feature_words()
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
        
    
    def get_feature_words(self, feature, topn=None):
        '''
            Gives words most closely associated with a given feature.
            Input:
                feature: number corresponding to the desired feature.
                topn: number of document ids to return.
        '''
        self._has_feature_words()
        assert(feature >= 0 and feature < self.Nfeat)
        
        topwords = self.feature_words.loc[feature,:].sort_values(ascending=False)
        return topwords[:topn]
    

        
    def get_word_features(self, word, topn=None):
        '''
            Gives features most closely associated with a given word.
            Input:
                word: word (or arbitrary basis name) to get features of.
                topn: number of feature ids to return.
        '''
        self._has_feature_words()
        assert(word in self.feature_words.columns)
        
        # series specifying values for each document along the particular feature
        topfeat = self.feature_words.loc[:,word].sort_values(ascending=False)
        return topfeat[:topn]
    
    

    
    def set_docnames(self,newdocnames):
        self.doc_features.index = newdocnames
        self.docnames = newdocnames
        
    def transform(self, bows, docnames=None, lang='en'):
        if self.model is None or self.vectorizer is None:
            raise Exception('Need to provide model & vectorizer in DocModel constructor to use .transform()')
        
        if docnames is None:
            docnames = list(range(len(bows)))
        
        # tokenize texts
        corpus = self.vectorizer.transform(bows)
        
        # actually construct dotopics
        doc_features = self.model.transform(corpus)
        
        # return dataframe
        return pd.DataFrame(doc_features,index=docnames)
    
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
    

        

    

        