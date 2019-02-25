import pandas as pd

class DocModel:
    '''
        This class contains a representation of documents in a corpus.
        It is currently being used for LDA and NMF topic models and Glove
            document representations.
    '''
    def __init__(self, doc_features, feature_words, vocab, docnames=None, model=None):
        
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
        ''' Gives docs most closely associated with a given feature. '''
        assert(feature >= 0 and feature < self.Nfeat)
        
        # series specifying values for each document along the particular feature
        topdocs = self.doc_features.loc[feature].sort_values(ascending=False)
        return topdocs[:topn]
    
    def get_feature_words(self, feature, topn=None):
        ''' Gives words most closely associated with a given feature. '''
        assert(feature >= 0 and feature < self.Nfeat)
        
        topwords = self.feature_words.loc[feature,:].sort_values(ascending=False)
        return topwords[:topn]
    
    def get_doc_features(self, doc, topn=None):
        ''' Gives features most closely associated with a given doc. '''
        assert(doc in self.docnames)
        
        # series specifying values for each document along the particular feature
        topfeat = self.doc_features.loc[doc,:].sort_values(ascending=False)
        return topfeat[:topn]
        
    def get_word_features(self, word, topn=None):
        ''' Gives features most closely associated with a given word. '''
        assert(word in self.feature_words.columns)
        
        # series specifying values for each document along the particular feature
        topfeat = self.feature_words.loc[:,word].sort_values(ascending=False)
        return topfeat[:topn]
    
    
    # ________ Create Summary Spreadsheets _________
    def feature_words_summary(self,topn=None):
        ''' Shows words most closely associated with each feature. '''
        
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
        ''' Shows features most closely associated with each document. '''
        
        if topn is None:
            topn = self.Nfeat
        
        df = pd.DataFrame(index=self.docnames, columns=range(topn))
        df.index.name = 'document'
        df.columns.name = 'nth top feature'
        for doc in self.docnames:
            topfeat = self.get_doc_features(doc, topn)
            df.loc[doc,:] = list(topfeat.index)
        
        return df
        
        
    def add_report(self, writer):
        
        writer = ExcelWriter(outfile)
        self.topics.to_excel(writer,'topics')
        self.docs.to_excel(writer,'docs')

        writer.save()
