import pandas as pd
import os.path
import spacy
import itertools

from .reports import write_report

class DocModel:
    '''
        This class contains a representation of documents in a corpus according
            to some number of dimensions.
        It is currently being used for LDA and NMF topic models and Glove
            document representations.
    '''
    def __init__(self, doc_features, feature_basis=None, docnames=None, featnames=None, basisnames=None, df_type=pd.SparseDataFrame, vectorizer=None, model=None):
        
        '''
            Represents Nd documents according to Nf features which are composed
                of Nt tokens (or an arbitrary basis set).
                
            Inputs:
                doc_features: <Nd x Nf> matrix of document representations.
                    (i.e. topic distributions, embedding vectors, etc)
                feature_words: <Nf x Nt> matrix of feature representations
                    in terms of tokens (or some arbitrary basis more generally).
                docnames: a convenient input of document names that will be 
                    return in class methods.
                model: arbitrary object for storing original sklearn LDA, NMF
                    or glove models with associated training parameters.
                dat: arbitrary data for docmodel storage. One may, for instance,
                    want to attach data from a model which is output from an algorithm
                        such as lda or nmf which can be used later.
        '''
        
        # convert doc_features to dataframe
        if isinstance(doc_features, pd.DataFrame) or isinstance(doc_features, list):
            self.doc_feat = df_type(doc_features)
            self.doc_feat.columns.name = 'feature'
            self.doc_feat.index.name = 'docname'
        else:
            # create dataframe with provided docnames and featnames
            self.doc_feat = df_type(doc_features)
            
            docrange = list(range(doc_features.shape[0]))
            docnames = list(docnames) if docnames is not None else docrange
            
            featrange = list(range(doc_features.shape[1]))
            featnames = list(featnames) if featnames is not None else featrange
            
            self.doc_feat.index = docnames
            self.doc_feat.index.name = 'docname'
            self.doc_feat.columns = featnames
            self.doc_feat.columns.name = 'feature'
            
        self.Ndocs = self.doc_feat.shape[0]
        self.Nfeat = self.doc_feat.shape[1]
            
            
        # format feature_basis dataframe
        self.feat_basis = None #(in case not assigned later)
        self.Nbasis = None
        if feature_basis is not None:
            assert(doc_features.shape[1] == feature_basis.shape[0])
            
            if isinstance(feature_basis, pd.DataFrame) or isinstance(doc_features, list):
                self.feat_basis = df_type(feature_basis)
                self.feat_basis.columns.name = 'feature'
                self.feat_basis.index.name = 'docname'
            else:
                self.feat_basis = df_type(feature_basis)
                
                basisrange = list(range(feature_basis.shape[1]))
                basisnames = list(basisnames) if basisnames is not None else basisrange
                
                self.feat_basis.index = self.doc_feat.columns
                self.feat_basis.columns = basisnames
                self.feat_basis.columns.name = 'basis'
                
            self.Nbasis = self.feat_basis.shape[1]
            
        
        # optional data for storage
        self.vectorizer = vectorizer
        self.model = model
        self.df_type = df_type
        
    
    def check_feat_basis(self):
        if self.feat_basis is None:
            raise Exception('feature_basis has not been provided.')
            
    
    # ________ Access Dataframe Features _________
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
                
        return self.get_row(self.doc_feat, doc, sort=sort, topn=topn)
    
        
    def get_feature_docs(self, feature, sort=False, topn=None):
        '''
            Gives documents most closely associated with a given feature.
            Input:
                feature: feature id to retrieve.
                topn: number of document ids to return.
        '''
        
        return self.get_row(self.doc_feat.T, feature, sort=sort, topn=topn)
    
    
    def get_feature_basis(self, feature, sort=False, topn=None):
        '''
            Gives documents most closely associated with a given feature.
            Input:
                feature: feature id to retrieve.
                topn: number of document ids to return.
        '''
        self.check_feat_basis()
        
        return self.get_row(self.feat_basis, feature, sort=sort, topn=topn)
        
    @staticmethod
    def get_row(df, ind, sort=True, topn=None):
        '''
            Utility function that returns row(s) or column(s) of
                df, either sorted or not. Used in get_doc_features
                and other similar functions.
            Input:
                df: dataframe of values (feat_basis or doc_feat)
                ind: index of row/col (on axis) to be extracted
                sort: return feat most closely associated with 
                    the doc.
                topn: number of feature ids to return.
        '''
        assert(ind in df.index)
        if not sort:
            return df.loc[ind,:]
        else:
            top = df.loc[ind,:].sort_values(ascending=False)
            return top[:topn]
        
    
    # ________ Create Summary DataFrames _________
    
    def get_doc_summary(self, topn=None, human=False):
        '''
            Creates dataframe listing features most closely associted
                with each doc.
            topn: max number of features to list for each doc.
            Inputs:
                topn: number of feature ids to return.
                human: T/F output human readable series
        '''
        df = self.get_summary(self.doc_feat, topn=topn, human=human)
        
        return df
        
        
    def get_feature_doc_summary(self, topn=None, human=False):
        '''
            Creates a summary of docs most closely associated with each feature.
            Inputs:
                topn: number of feature ids to return.
                human: T/F output human readable series
        '''

        df = self.get_summary(self.doc_feat.T, topn=topn, human=human).T
        
        return df
    
    def get_feature_summary(self, topn=None, human=False):
        '''
            Creates a summary basis objects most closely associated
                with each feature.
            Inputs:
                topn: number of feature ids to return.
                human: T/F output human readable series
        '''
        self.check_feat_basis()

        df = self.get_summary(self.feat_basis, topn=topn, human=human)
        
        return df
        
    def get_summary(self, df, topn=None, human=False):
        '''
            Utility function that summarizes df by sorting 
                rows. To sort by columns, simply transpose the input
                dataframe before passing to this function.
                TODO: better description
            Input:
                df: dataframe of values (feat_basis or doc_feat)
                topn: number of feature ids to return.
                human: T/F output human readable series
        '''
        if not human:
            if topn is None:
                columns = range(df.shape[1])
            else:
                columns = range(topn)
            
            # summaries by placing index values into dataframe
            summary_df = pd.DataFrame(index=df.index, columns=columns)
            summary_df.columns.name = 'nth_closest'
            for ind in df.index:
                row = self.get_row(df, ind, sort=True, topn=topn)
                summary_df.loc[ind,:] = list(row.index)
            return summary_df
        
        else:
            
            # create multiindex for human summary
            prod = itertools.product(df.index, df.columns)
            mi = pd.MultiIndex.from_tuples(list(prod))
            hs = pd.Series(df.values.flatten(),index=mi)

            # sort on values and then index
            hs = hs.sort_values(ascending=False)
            hs = hs.sort_index(level=0, sort_remaining=False)
            hs = hs.dropna()
            
            # adding totals rows
            totcolname = '__Totals__'
            #tots = df.sum(axis=0).sort_values(ascending=False)
            tots = df.sum(axis=0,skipna=True)#.sort_values(ascending=False)
            tmi = pd.MultiIndex.from_tuples([(totcolname, c) for c in df.columns])
            ts = pd.Series(tots.values,index=tmi).sort_values(ascending=False)
            hs = ts.append(hs)
            
            return hs
        
        
    
    # ---------- Other Functions ----------
    
    def transform(self, bows, docnames=None, lang='en'):
        '''
            Utility function that summarizes df by sorting 
                rows/columns. Needs .model and .vectorizer
                to be provided. Custom objects can be provided
                as long as they have .transform() methods.
            Input:
                df: dataframe of values (feat_basis or doc_feat)
                axis: basis axis to sort from. 0 means it will keep
                    rows and sort columns for each row. 1 is vice-versa.
                topn: number of feature ids to return.
        '''
        
        if self.model is None or self.vectorizer is None:
            raise Exception('Need to provide model & vectorizer \
                    in DocModel constructor to use .transform()')
        
        if docnames is None:
            docnames = list(range(len(bows)))
        
        # tokenize texts
        corpus = self.vectorizer.transform(bows)
        
        # actually construct dotopics
        doc_features = self.model.transform(corpus)
        
        # return dataframe
        df = self.df_type(doc_features, index=docnames, columns=self.doc_feat.columns)
        df.index.name = 'docname'
        return df
    
    
    
