import os
import pandas as pd

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
                if verbose: print('saving as hdf instead.')
                path, file = os.path.split(fname)
                base, ext = os.path.splitext(file)
                
                newfname = path + base + '.h5'
                if os.path.isfile(newfname):
                    i = 1
                    while os.path.isfile(newfname):
                        newfname = path + base + '_{}.h5'.format(i)
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

def write_excel(fname,sheets,topn=None,):
    
    writer = pd.ExcelWriter(fname)
    for sheetname, sheetdf in sheets:
        sheetdf.to_excel(writer,sheetname)
    writer.save()
        
                

def write_hdf(fname, sheets, topn=None):
    '''
        Write to hdf file according to sheetnames.
    '''
    for sheetname, sheetdf in sheets:
        sheetdf.to_hdf(fname, sheetname)

        



def make_human_report(ctlist, names):
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
            
    #df['docname'] = df.index.get_level_values('docname')
    df = df.sort_values(['docname','count'],ascending=[True,False])
    #del df['docname']
            
    return df

def count_totals(allcts):
    totals = dict()
    for cts in allcts:
        for n,ct in cts.items():
            if n not in totals.keys():
                totals[n] = 0
            totals[n] += ct
    return totals