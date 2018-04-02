from __future__ import with_statement
from distutils.core import setup

import paired


with open('README.md', 'r') as f:
    long_description = f.read()

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: CPython',
]

project_urls = {
    'Documentation': 'https://github.com/ajnisbet/paired',
    'Source': 'https://github.com/ajnisbet/paired',
}

setup(
    name='paired',
    author='Andrew Nisbet',
    version=paired.__version__,
    py_modules=['paired'],
    tests_require=['pytest'],
    description='Sequence alignment of Python objects.',
    long_description=long_description,
    license='MIT',
    url='https://github.com/ajnisbet/paired',
    classifiers=classifiers,
    project_urls=project_urls,
)
