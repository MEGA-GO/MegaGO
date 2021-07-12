#!/usr/bin/env python

from setuptools import setup

LONG_DESCRIPTION = \
'''
Mega-GO calculates the similarity between GO terms with the relevance semantic similarity (sim<sub>Rel</sub>) metric.
The program reads one or more input FASTA files.
For each file it computes a variety of statistics, and then
prints a summary of the statistics as output.

The goal is to provide a solid foundation for new bioinformatics command line tools,
and is an ideal starting place for new projects.'''


setup(
    name='megago',
    version='0.5.0.2021.01.2021.01.2021.02.2021.03.2021.03',
    author='Henning Schiebenhoefer',
    author_email='henning.schiebenhoefer@posteo.de',
    packages=['megago'],
    package_dir={'megago': 'megago'},
    package_data={'megago': [
        "resources/associations-uniprot-sp-20200116.tab",
        "resources/go-basic.obo",
        "resources/frequency_counts_uniprot.json",
        "resources/highest_ic_uniprot.json",
        "resources/heatmap_template.html"
    ]},
    entry_points={
        'console_scripts': ['megago = megago.megago:main']
    },
    url='https://github.com/MEGA-GO/megago',
    license='LICENSE',
    description=('Calculate semantic distance for sets of Gene Ontology terms'),
    long_description=(LONG_DESCRIPTION),
    install_requires=[
        "goatools",
        "seaborn",
        "progress"
    ],
)
