
from setuptools import setup

setup(name='easytext',
    version='0.1',
    description='Simple text analysis tools.',
    url='https://github.com/devincornell/easytext',
    author='Devin J. Cornell',
    author_email='devinj.cornell@gmail.com',
    license='MIT',
    packages=['easytext'],
    install_requires=[
        'sklearn',
        'spacy',
        'pandas',
        'numpy',
        'glove',
    ]
    zip_safe=False)


