import json
import os

from goatools.anno.idtogos_reader import IdToGosReader
from goatools.obo_parser import GODag
from goatools.semantic import TermCounts
from progress.bar import IncrementalBar

from .constants import FREQUENCY_COUNTS_FILE_PATH, UNIPROT_ASSOCIATIONS_FILE_PATH, GO_DAG_FILE_PATH


def _precompute_term_frequencies():
    print("Start precomputations of term frequencies...")
    go_freq_dict = dict()
    go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))

    associations = IdToGosReader(UNIPROT_ASSOCIATIONS_FILE_PATH, godag=go_dag).get_id2gos('all')
    term_counts = TermCounts(go_dag, associations)

    for i in go_dag.values():
        go_freq_dict[i.id] = term_counts.get_count(i.id)
        for alt_id in i.alt_ids:
            go_freq_dict[alt_id] = term_counts.get_count(i.id)
    # write frequency dict to JSON file
    with open(FREQUENCY_COUNTS_FILE_PATH, 'w') as json_file:
        json.dump(go_freq_dict, json_file)


def get_frequency_counts():
    """ This function precomputes the term frequency counts if these are outdated or not present. If they are present and
    valid, it will directly return the frequency counts.

    Returns
    -------
    A dictionary that maps each GO-term onto it's frequency counts.
    """
    if not os.path.isfile(FREQUENCY_COUNTS_FILE_PATH):
        _precompute_term_frequencies()

    frequency_dict = json.load(open(FREQUENCY_COUNTS_FILE_PATH))
    return frequency_dict


if __name__ == "__main__":
    get_frequency_counts()
