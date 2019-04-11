
from setuptools import setup

setup(
    name='easytext',
    packages=['easytext',],
    version='0.1',
    license='MIT',
    description='Simple text analysis tools with command line interface that writes to excel files.',
    url='https://github.com/devincornell/easytext',
    author='Devin J. Cornell',
    author_email='devinj.cornell@gmail.com',
    download_url = 'https://github.com/devincornell/easytext/archive/v0.1.tar.gz',
    keywords=[
        'text analysis', 
        'topic modeling', 
        'parse trees', 
        'educational',
    ],
    install_requires=[
        'sklearn',
        'spacy',
        'pandas',
        'numpy',
        'glove_python',
        'empath',
    ],
    zip_safe=False,
)


