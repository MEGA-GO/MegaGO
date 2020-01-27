from goatools.obo_parser import GODag
from goatools.anno.idtogos_reader import IdToGosReader
from goatools.semantic import deepest_common_ancestor, get_info_content, TermCounts
import time
import multiprocessing

from argparse import ArgumentParser
from math import floor
import sys
import logging
import pkg_resources
import os

EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
EXIT_FASTA_FILE_ERROR = 3
DEFAULT_MIN_LEN = 0
DEFAULT_VERBOSE = False
HEADER = 'FILENAME\tNUMSEQ\tTOTAL\tMIN\tAVG\tMAX'
PROGRAM_NAME = "megago"
DATA_DIR = pkg_resources.resource_filename(__name__, 'resource_data')

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"

GODAG = GODag(os.path.join(DATA_DIR, "go-basic.obo"))
UNIPROT_ASSOCIATIONS_FILE = os.path.join(DATA_DIR, "associations-uniprot-sp-20200116.tab")


def read_input(file_path):
    """
    This function reads a csv with two columns of GO terms, coming from two datasets
    Returns two lists of GO terms
    """

    GO_list1, GO_list2 = list(), list()

    with open(file_path, "r", encoding='utf-8-sig') as in_f:  # other files might require other encoding?
        for line in in_f:
            if not line.startswith("GO"):  # skip header
                continue
            GO1, GO2, _ = line.strip().split(",", maxsplit=2)

            # add GO1 to GO_list1
            GO1_sub = list()
            if ";" in GO1:
                mGO = GO1.split(";")
                for GO in mGO:
                    GO1_sub.append(GO)
            else:
                GO1_sub.append(GO1)
            GO_list1.append(GO1_sub)

            # add GO2 to GO_list2
            GO2_sub = list()
            if ";" in GO2:
                mGO = GO2.split(";")
                for GO in mGO:
                    GO2_sub.append(GO)
            else:
                GO2_sub.append(GO2)
            GO_list2.append(GO2_sub)

        return GO_list1, GO_list2


def BMA(GO_list1, GO_list2, termcounts, similarity_method=None):
    summationSet12 = 0.0
    summationSet21 = 0.0
    for id1 in GO_list1:
        similarity_values = []
        for id2 in GO_list2:
            similarity_values.append(Rel_Metric(id1, id2, GODAG, termcounts))
        summationSet12 += max(similarity_values)
    for id2 in GO_list2:
        similarity_values = []
        for id1 in GO_list1:
            similarity_values.append(Rel_Metric(id2, id1, GODAG, termcounts))
        summationSet21 += max(similarity_values)
    return (summationSet12 + summationSet21) / (len(GO_list1) + len(GO_list2))


def Rel_Metric(id1, id2, godag, termcounts):
    if id1 == '' or id2 == '':
        return -1
    goterm1 = godag[id1]
    goterm2 = godag[id2]
    if goterm1.namespace == goterm2.namespace:
        mica_goid = deepest_common_ancestor([id1, id2], godag)
        freq = termcounts.get_term_freq(mica_goid)
        infocontent = get_info_content(mica_goid, termcounts)
        infocontent1 = get_info_content(id1, termcounts)
        infocontent2 = get_info_content(id2, termcounts)
        return (2 * infocontent * (1 - freq)) / (infocontent1 + infocontent2)
    else:
        return -1


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Calculate semantic distance for sets of Gene Ontology terms'
    parser = ArgumentParser(description=description)
    # parser.add_argument(
    #     '--minlen',
    #     metavar='N',
    #     type=int,
    #     default=DEFAULT_MIN_LEN,
    #     help='Minimum length sequence to include in stats (default {})'.format(
    #         DEFAULT_MIN_LEN))
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
                        metavar='LOG_FILE',
                        type=str,
                        help='record program progress in LOG_FILE')
    parser.add_argument('input_table',
                        metavar='INPUT_TABLE',
                        type=str,
                        help='Input table file')
    return parser.parse_args()


def run_comparison(options):
    def process(go1, go2, termcounts):
        BMA_test = BMA(go1, go2, termcounts)
        print(BMA_test)

    GO_list1, GO_list2 = read_input(options.input_table)
    associations = IdToGosReader(UNIPROT_ASSOCIATIONS_FILE, godag=GODAG).get_id2gos('all')

    termcounts = TermCounts(GODAG, associations)

    jobs = []

    start = time.time()

    for i in range(0, len(GO_list1)):
        print(f"Computing {i}")
        p = multiprocessing.Process(target=process, args=(GO_list1[i], GO_list2[i], termcounts))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    end = time.time()
    print(str(end - start) + " s")


def main():
    options = parse_args()
    # init_logging(options.log)
    run_comparison(options)


if __name__ == "__main__":
    main()
