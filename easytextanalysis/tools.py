import pandas as pd
from collections.abc import Iterable



def main(texts, nlp=None):
    
    # docs should be iterable run after pipe function
    # CAN ONLY DO THIS LOOP ONCE!
    Doc.set_attribute('entverbs', default=False)

    nlp = spacy.load('en')
    doc = nlp(u'hello world')
    doc._.is_greeting = True



















def count_totals(allcts):
    totals = dict()
    for cts in allcts:
        for n,ct in cts.items():
            if n not in totals.keys():
                totals[n] = 0
            totals[n] += ct
    return totals


def dict2df(ctlist, names):
    '''
    Converts list of dictionaries into flattened dataframe.
    '''
    #Nrows = sum([len(cts) for cts in ctlist])
    ind = [(nm,i) for cts,nm in zip(ctlist,names) for i in range(len(cts))]
    mi = pd.MultiIndex.from_tuples(ind).rename(('docname','val_id'),)
    df = pd.DataFrame(index=mi, columns=('doc','value','count'))
    
    for i,cts in enumerate(ctlist):
        sortcts = list(sorted(cts.items(), key=lambda x: x[1], reverse=True))
        nvals = len(sortcts)
        for j in range(nvals):
            value = sortcts[j][0]
            #if isinstance(value,str):
            #    useval = value
            #elif isinstance(value,Iterable):
            #    useval = ','.join(value)
            #else:
            useval = value
            
            ind = (names[i],j)
            df.loc[ind,'doc'] = names[i]
            df.loc[ind,'value'] = useval
            df.loc[ind,'count'] = sortcts[j][1]
            
    return df
    



