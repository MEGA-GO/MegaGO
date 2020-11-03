# This script precomputes all comparison values for the complete set of GO-terms. We only calculate and store the
# comparison value of two GO-terms in the same namespace, as terms from different namespaces cannot be compared with
# each other.

import math
import json
import os
import concurrent.futures

from goatools.obo_parser import GODag
from progress.bar import IncrementalBar

from .constants import GO_DAG_FILE_PATH, HIGHEST_IC_FILE_PATH
from .precompute_frequency_counts import get_frequency_counts
from .metrics import get_ic_of_most_informative_ancestor

# How large should the chunks be in which the list of terms for which ic needs to be computed should be divided?
CHUNK_SIZE = 500

# How many processes can be used simultaneously at maximum? (Set to none for default)
PROCESSES = None


def _do_compute_highest_inc(terms):
    term_counts = get_frequency_counts()
    go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))
    return {term: get_ic_of_most_informative_ancestor(term, term_counts, go_dag) for term in terms}


def compute_highest_inc_parallel(terms):
    """ Compare all values from the given terms set in parallel by using up to PROCESSES processes simultaneously.
    Params
    ------
    terms: A list with GO-terms for which the information content should be precomputed.
    """
    print("Start precomputations of the highest_inc_anc for all GO-terms.")

    term_len = len(terms)
    highest_ic_anc = dict()

    amount_of_chunks = math.ceil(term_len / CHUNK_SIZE)

    # Effectively compute the comparisons
    with concurrent.futures.ProcessPoolExecutor(max_workers=PROCESSES) as executor:
        bar = IncrementalBar('Processing', max=amount_of_chunks, suffix='%(percent)d%% - Elapsed: %(elapsed)ds - Remaining: %(eta)ds')
        for result in executor.map(_do_compute_highest_inc, (terms[i:i + CHUNK_SIZE] for i in range(0, term_len, CHUNK_SIZE))):
            bar.next()
            highest_ic_anc.update(result)
        bar.finish()

    with open(HIGHEST_IC_FILE_PATH, 'w') as json_file:
        json.dump(highest_ic_anc, json_file)


def get_highest_ic():
    if not os.path.isfile(HIGHEST_IC_FILE_PATH):
        go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))
        compute_highest_inc_parallel(list(go_dag.keys()))

    ic_file = open(HIGHEST_IC_FILE_PATH, 'r')
    highest_ic_anc = json.load(ic_file)
    ic_file.close()

    return highest_ic_anc


if __name__ == "__main__":
    get_highest_ic()
