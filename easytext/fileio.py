
import os.path
import pandas as pd


def filenames_to_docnames(fnames):
    '''
        Convert original file names to more readable names
            wile checking to make sure there are no collisions.
    '''
    newnames = list()
    for fn in fnames:
        base = os.path.basename(fn)
        basename = os.path.splitext(base)[0]
        newnames.append(basename)
    
    # check and make sure it didn't wipe out any redundancies
    # (this could happen if pulling from multiple folders or catching multiple file extensions)
    if len(set(newnames)) != len(newnames):
        newnames = fnames
    
    return newnames
        
def read_text_file(fname):
    with open(fname, 'rb') as f:
        text = f.read().decode('ascii',errors='ignore')
    return text


def read_input_files(infiles,doclabelcol,textcol):
    '''
        Reads single or multiple text files or an excel/csv file.
    '''
    
    # read multiple text files
    if len(infiles) > 1:
        texts = [read_text_file(fn) for fn in infiles]
        docnames = filenames_to_docnames(infiles)
    
    else:
        fname = infiles[0]
        fext = os.path.splitext(os.path.basename(fname))[1]
        
        # read single text file
        if fext == '.txt':
            text = read_text_file(fname)
            textnames = [(i,t) for i,t in enumerate(text.split('\n')) if len(t) > 0]
            docnames = [str(i) for i,t in textnames]
            texts = [t for i,t in textnames]
            
        # read spreadsheet file using pandas
        elif fext in ('.xlsx','.xls','.csv',):
            try:
                if fext == '.csv':
                    df = pd.read_csv(fname)
                elif fext in ('.xlsx','.xls'):
                    df = pd.read_excel(fname)
            except:
                raise Exception('There was a problem reading the {} file.'.format(fext))
                
            # perform checks on column names
            if textcol not in df.columns:
                raise Exception('The text column name was not found in spreadsheet:', textcol)
            if doclabelcol is not None and doclabelcol not in df.columns:
                raise Exception('The column name for document labels was not found in the spreadsheet:', doclabelcol)
                
            # extract texts and doclabels
            texts = [str(v) for v in df[textcol]]
            if doclabelcol is not None:
                docnames = [str(n) for n in df[doclabelcol]]
            else:
                docnames = [str(i) for i in range(df.shape[0])]

        else:
            raise Exception('You need to pass an xls or 1+ txt files.')
            
    return texts, docnames

