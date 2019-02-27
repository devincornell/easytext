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
            #if verbose: print('Successfully wrote as excel:', fname)
        except AttributeError:
            # weird error where dataframes are too big
            
            if hdf_if_fail:
                print('ran into issue: desired output file is too big for excel sheet.')
                print('saving as hdf instead.')
                # change filename to an .h5 that doesn't exist
                #basename = os.path.splitext(fname)[0]
                path, file = os.path.split(fname)
                base, ext = os.path.splitext(file)
                
                #newfname = os.rename(fname, basename + '.h5')
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
        #if verbose: print('saved file as hdf:', fname)
    else:
        raise Exception('File extension {} was not recognized as a valid output format.'.format(fext))
    
    return final_fname

def write_excel(fname,sheets,topn=None,):
    
    # this function is wrapped in try-catch so can revert to hdf if needed
    #with pd.ExcelWriter(fname) as writer:
    #    for sheetname, sheetdf in sheets:
    #        sheetdf.to_excel(writer,sheetname)
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
