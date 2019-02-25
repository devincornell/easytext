

from .grammar import *
from .ner import *
from .tools import *
from .easytext import *
from .algorithms import *



'''
from spacy.language import Language
for name,comp in EASYTEXT_ALL_COMPONENTS.items():
    Language.factories['easytext-'+name] = lambda **kwargs: comp(**kwargs)
'''