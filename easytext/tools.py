
import pandas as pd
from collections.abc import Iterable

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
    totalcts = count_totals(ctlist)
    
    ind = [(nm,i) for cts,nm in zip(ctlist,names) for i in range(len(cts))] + \
            [('Totals',i) for i in range(len(totalcts))]
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
    
    df.loc[['Totals',],'doc'] = 'Totals'
    #for 
    
    #df.loc[('_Totals_',0),'doc'] = '_Totals_'
    #df.loc[('_Totals_',0),value] = '_Totals_'
    #df.loc[('_Totals_',0),'doc'] = '_Totals_'
            
    return df
    
    
    
    
def dict2df(ctlist, names):
    '''
        Converts list of dictionaries into flattened dataframe.
    '''
    #Nrows = sum([len(cts) for cts in ctlist])
    totalcts = count_totals(ctlist)
    
    allnames = list(names) + ['Totals',]
    allcts = list(ctlist) + [totalcts,]
    
    ind = [(nm,val) for nm,valcts in zip(allnames,allcts) for val,ct in valcts.items()]
    mi = pd.MultiIndex.from_tuples(ind).rename(('docname','value'),)
    df = pd.DataFrame(index=mi, columns=('count',))
    
    for nm,valcts in zip(allnames,allcts):
        for val,ct in valcts.items():
            df.loc[(nm,val),'count'] = ct
            
    df['docname'] = df.index.get_level_values('docname')
    df = df.sort_values(['docname','count'],ascending=[True,False])
    del df['docname']
            
    return df#.sort_values(['count',],ascending=False)



