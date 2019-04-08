from empath import Empath
import re
import pandas as pd
import spacy
from collections import Counter

from .algorithms import glove, lda, nmf
from .reports import write_report, make_human_report, make_summary
from .easytext import easyparse

def subcommand_wordcount(texts, docnames, args):
    #print('converting', len(texts), 'texts to bags-of-words')
    if args.words is not None:
        counts = list()
        twords = [w.strip() for w in args.words.split(',')]
        assert(len(twords) > 0)
        for pw in easyparse(nlp,texts,enable=['wordlist',]):
            if len(pw['wordlist']) > 0:
                wc = dict()
                for tword in twords:
                    wc[tword] = pw['wordlist'].count(tword)
                counts.append(wc)
    else:
        assert(args.min_tf > 0)
        print('Counting all words with min_tf of', args.min_tf)

        docbow = list()
        for pw in easyparse(nlp,texts,enable=['wordlist',]):
            if len(pw['wordlist']) > 0:
                docbow.append(pw['wordlist'])
        freq = Counter([w for d in docbow for w in d])
        twords = [w for w,c in freq.items() if c >= args.min_tf]
        print('Kept', len(twords), 'words in vocab to count.')
        counts = list()
        for bow in docbow:
            wc = dict()
            for tword in twords:
                wc[tword] = bow.count(tword)
            counts.append(wc)

    # build output sheets
    sheets = list()
    df = pd.DataFrame(counts,index=docnames)
    if args.human_readable:
        hdf = make_human_report(df)
        sheets.append(('humancounts',hdf))
    else:
        sheets.append(('counts',df))

    # actually write report
    final_fname = write_report(
        args.outfile, 
        sheets, 
        hdf_if_fail=not args.nohdfonfail and not args.human_readable, 
        verbose=True,
    )

    return final_name


def subcommand_sentiment(texts, docnames, args):
    lexicon = Empath()
    if args.posneg_only:
        cats = ['positive_emotion','negative_emotion']
    else:
        cats = None # all the categories

    analyze = lambda t: lexicon.analyze(t, categories=cats, normalize= not args.no_normalize)
    sentiments = [analyze(t) for t in texts]


    df = pd.DataFrame(sentiments,index=docnames)
    summarydf = make_summary(df)

    sheets = list()
    if args.human_readable:
        hdf = make_human_report(df)
        sheets.append( ('report',hdf) )
    else:
        sheets.append( ('report',df))
    sheets.append(('summary',summarydf))

    final_fname = write_report(
        args.outfile, 
        sheets, 
        hdf_if_fail=not args.nohdfonfail and not args.human_readable, 
        verbose=True,
    )

    return final_name




def subcommand_entities(texts, docnames, args):
    assert(args.min_tf > 0)
    assert(not (args.ignore_types is not None and args.use_types is not None))

    # decide which entities to use
    if args.use_types is not None:
        pipeargs = {'use_ent_types': [t.strip() for t in args.use_types.split(',')]}
    if args.ignore_types is not None:
        pipeargs = {'ignore_ent_types': [t.strip() for t in args.ignore_types.split(',')]}
    else:
        # by default, remove these:
        ignorelist = 'DATE,TIME,PERCENT,MONEY,QUANTITY,ORDINAL,CARDINAL'
        pipeargs = {'ignore_ent_types': [t.strip() for t in ignorelist.split(',')]}

    # parse all entities
    docents = list()
    for pw in easyparse(nlp,texts,enable=['entlist',],pipeargs=pipeargs):
        if len(pw['entlist']) > 0:
            docents.append([n for n,e in pw['entlist']])

    # determine ents to count
    freq = Counter([e for d in docents for e in d])
    tents = [w for w,c in freq.items() if c >= args.min_tf]
    if len(tents) == 0:
        raise Exception('No ents reached the count threshold given.')
    print('Kept', len(tents), 'entities to count.')

    # count entities per-doc
    counts = list()
    for ents in docents:
        wc = dict()
        for tent in tents:
            wc[tent] = ents.count(tent)
        counts.append(wc)


    # build output sheets
    sheets = list()
    df = pd.DataFrame(counts,index=docnames)
    if args.human_readable:
        hdf = make_human_report(df)
        sheets.append(('humanents',hdf))
    else:
        sheets.append(('ents',df))

    # actually write report
    final_fname = write_report(
        args.outfile, 
        sheets, 
        hdf_if_fail=not args.nohdfonfail and not args.human_readable, 
        verbose=True,
    )
    return final_name






def subcommand_topicmodel(texts, docnames, args):
    assert(args.numtopics > 0)
    assert(args.type.lower() in ('lda','nmf'))
    assert(args.numtopics < len(texts))

    print('converting', len(texts), 'texts to bags-of-words')
    bows = list()
    for pw in easyparse(nlp,texts,enable=['wordlist',]):
        if len(pw['wordlist']) > 0:
            bows.append(pw['wordlist'])

    print('performing topic modeling with', args.numtopics, 'topics.')
    tmfunc = nmf if args.type.lower() == 'nmf' else lda
    model = tmfunc(
        docbows=bows, 
        n_topics=args.numtopics, 
        docnames=docnames,
        min_tf=args.min_tf,
        random_state=args.seed,
    )

    print('writing output report')
    final_fname = model.write_report(
        args.outfile, 
        save_wordmatrix=not args.nosave_wordmatrix, 
        featurename='topic',
        hdf_if_fail = not args.nohdfonfail,
    )
    return final_name



def subcommand_glove(texts, docnames, args):
    assert(args.dimensions > 0)
    assert(args.dimensions < len(texts))
    keywords = parse_keywords(args.keywords)

    # parse texts using spacy
    print('converting', len(texts), 'texts to sentence lists')
    docsents = list()
    for pw in easyparse(nlp,texts,enable=['sentlist']):
        if len(pw['sentlist']) > 0:
            docsents.append(pw['sentlist'])

    print('running glove algorithm with n =', args.dimensions)
    model = glove(
        docsents, 
        args.dimensions,
        docnames=docnames,
        keywords=keywords,
        min_tf=args.min_tf,
    )

    print('writing output report to', args.outfile)
    final_fname = model.write_report(
        args.outfile, 
        save_wordmatrix= not args.nosave_wordmatrix, 
        featurename='dimension',
        hdf_if_fail = not args.nohdfonfail,
    )
    
    return final_name

























