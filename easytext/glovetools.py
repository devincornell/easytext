
from glove.glove_cython import fit_vectors, transform_paragraph
import collections
import numpy as np

#print(glove.transform_paragraph(test))
#def glove_transform_paragraph(gm, )

def glove_vector(gm,word):
    ind = gm.dictionary[word]
    return gm.word_vectors[ind]

def glove_projection(gm, tword, pvec):
    tvec = glove_vector(gm,tword)
    print(pvec.shape)
    prod = pvec.dot(tvec)/(np.linalg.norm(tvec) * np.linalg.norm(pvec))
    return prod


def check_random_state(seed):
    """ Turn seed into a np.random.RandomState instance.
        This is a copy of the check_random_state function in sklearn
        in order to avoid outside dependencies.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)



def glove_transform_paragraph(gm, paragraph, epochs=50, ignore_missing=False):
    """
    Transform an iterable of tokens into its vector representation
    (a paragraph vector).
    Experimental. This will return something close to a tf-idf
    weighted average of constituent token vectors by fitting
    rare words (with low word bias values) more closely.
    """

    if gm.word_vectors is None:
        raise Exception('Model must be fit to transform paragraphs')

    if gm.dictionary is None:
        raise Exception('Dictionary must be provided to '
                        'transform paragraphs')

    cooccurrence = collections.defaultdict(lambda: 0.0)

    for token in paragraph:
        try:
            cooccurrence[gm.dictionary[token]] += gm.max_count / 10.0
        except KeyError:
            if not ignore_missing:
                raise

    random_state = check_random_state(gm.random_state)

    word_ids = np.array(list(cooccurrence.keys()), dtype=np.int32)
    values = np.array(list(cooccurrence.values()), dtype=np.float64)
    shuffle_indices = np.arange(len(word_ids), dtype=np.int32)

    # Initialize the vector to mean of constituent word vectors
    paragraph_vector = np.mean(gm.word_vectors[word_ids], axis=0)
    sum_gradients = np.ones_like(paragraph_vector)

    # Shuffle the coocurrence matrix
    random_state.shuffle(shuffle_indices)
    transform_paragraph(gm.word_vectors,
                        gm.word_biases,
                        paragraph_vector,
                        sum_gradients,
                        word_ids,
                        values,
                        shuffle_indices,
                        gm.learning_rate,
                        gm.max_count,
                        gm.alpha,
                        epochs)

    return paragraph_vector


