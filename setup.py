"""
Based on https://github.com/pypa/sampleproject

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ink_extensions',
    version='2.1.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/evil-mad/ink_extensions',
    authors='Windell Oskay, Anna S Berleant, Claudia Pellegrino'

    packages=find_packages(exclude=['contrib', 'docs', 'test', 'test.*']),
    install_requires=[
        'lxml'
    ],
    extras_require={
        'dev': [
            'coverage', # coverage run -m unittest discover && coverage html
        ],
        'test': [
            'mock',
        ],
    },
)
