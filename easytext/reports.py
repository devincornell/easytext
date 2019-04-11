import os
import pandas as pd
import itertools

def write_report(fname, sheets, hdf_if_fail=True, verbose=True, **kwargs):
    '''
        Will write excel sheet file with sheets corresponding to keys of sheetnames.
    '''
    final_fname = fname
    fext =os.path.splitext(os.path.basename(fname))[1]
    if fext in ('.xls','.xlsx'):
        try:
            write_excel(fname, sheets,**kwargs)
        except AttributeError:
            # weird error where dataframes are too big
            
            if hdf_if_fail:
                if verbose: print('ran into issue: desired output file is too big for excel sheet.')
                if verbose: print('with topicmodel or glove subcommands you can use the flag "--nosave_wordmatrix" to reduce output size.')
                if verbose: print('saving as hdf instead.')
                path, file = os.path.split(fname)
                base, ext = os.path.splitext(file)
                
                newfname = os.path.join(path, base) + '.h5'
                if os.path.isfile(newfname):
                    i = 1
                    while os.path.isfile(newfname):
                        newfname = os.path.join(path, base) + '_{}.h5'.format(i)
                        i += 1
                
                write_hdf(newfname, sheets, **kwargs)
                final_fname = newfname
            else:
                raise Exception('problem saving as xls: file too big. To save as .hdf on fail, set --hdfiffail flag in command.')
                
    elif fext in ('.h5','.hdf'):
        write_hdf(fname, sheets, **kwargs)
    else:
        raise Exception('File extension {} was not recognized as a valid output format.'.format(fext))
    
    return final_fname

def write_excel(fname,sheets):
    '''
        Write excel file (usually called from write_report).
        inputs:
            fname: output file path
            sheets: tuple of name,dataframe pairs to add.
    '''
    
    writer = pd.ExcelWriter(fname)
    for sheetname, sheetdf in sheets:
        sheetdf.to_excel(writer,sheetname)
    writer.save()
        
                

def write_hdf(fname, sheets):
    '''
        Write hdf file (usually called from write_report).
        inputs:
            fname: output file path
            sheets: tuple of name,dataframe pairs to add.
    '''
    
    for sheetname, sheetdf in sheets:
        sheetdf.to_hdf(fname, sheetname)

        
def make_summary(df, show_n=30):
    '''
        Makes summary by sorting values in each row
            then listing top dimensions (or counts) in that document.
    '''
    ncols = min(show_n,len(df.columns))
    sdf = pd.DataFrame(index=df.index,columns=range(ncols))
    for ind in df.index:
        vals = df.loc[ind,:].sort_values(ascending=False)
        sdf.loc[ind,:] = list(vals.index)[:ncols]
    return sdf


def make_human_report(df):
    '''
        Creates human readable report from raw values dataframe,
            essentially by folding columns into multi-index then 
            sorting.
    '''
    
    indcolname = '__indexcol__' # remporary column for sorting
    valuescolname = 'values'
    totalsindname = '__Totals__'
    mi = pd.MultiIndex.from_tuples(list(itertools.product(map(str,df.index),df.columns)))
    hdf = pd.DataFrame(index=mi, columns=[valuescolname,indcolname])
    for doc,val in hdf.index:
        hdf.loc[(doc,val,),valuescolname] = df.loc[doc,val]
    
    # sort based on docs then values
    hdf[indcolname] = list(hdf.index.get_level_values(0))
    hdf = hdf.sort_values([indcolname,valuescolname],ascending=[True,False])
    hser = hdf[valuescolname]
    
    # create totals value at bottom
    totser = df.sum(axis=0).sort_values(ascending=False)
    mi = pd.MultiIndex.from_tuples([(totalsindname,c) for c in totser.index])
    totser.index = mi
    hser = hser.append(totser)
    
    return hser
    
    