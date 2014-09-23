from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name             = 'swissdutch',
    version          = '0.1.0',
    description      = 'An implementation of the Swiss Dutch pairing system in Python',
    long_description = long_description,
    url              = 'https://github.com/rmoritz/swissdutch',
    author           = 'Ralph Moritz',
    author_email     = 'ralphmoritz@outlook.com',
    license          = 'MIT',
    keywords         = ['swiss', 'pairing', 'dutch', 'system', 'chess', 'tournament'],
    packages         = ['swissdutch'],
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
)
