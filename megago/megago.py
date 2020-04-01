from goatools.obo_parser import GODag
from goatools.semantic import deepest_common_ancestor
from goatools.gosubdag.gosubdag import GoSubDag
from . import make_GO_freq_json
import time
import multiprocessing

import argparse
import numbers
import seaborn as sns
import sys
import logging
import pkg_resources
import os
import json
import math
import platform
import re

EXIT_COMMAND_LINE_ERROR = 2
EXIT_FASTA_FILE_ERROR = 3
DEFAULT_MIN_LEN = 0
DEFAULT_VERBOSE = False
HEADER = 'ID,SIMILARITY'
PROGRAM_NAME = "megago"
DATA_DIR = pkg_resources.resource_filename(__name__, 'resource_data')

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"

GODAG_FILE_PATH = os.path.join(DATA_DIR, "go-basic.obo")
UNIPROT_ASSOCIATIONS_FILE_PATH = os.path.join(DATA_DIR, "associations-uniprot-sp-20200116.tab")
JSON_INDEXED_FILE_PATH = os.path.join(DATA_DIR, "go_freq_uniprot.json")

def is_go_term(string):
    regex = re.compile(r"^go:\d{7}$", re.IGNORECASE)
    if regex.match(string):
        return True
    else:
        return False


def read_input(in_file, sep=",", go_sep=";"):
    """
    Read a csv with three columns: ID, GO terms 1, GO terms 2, coming from two datasets
    Arguments:
        in_file: an open file object
        sep: field separator of input file, default: ','
        go_sep: separator between individual go terms, default: ';'
    Result:
        id_list, two nested lists of GO terms
    """

    id_list, go_list1, go_list2 = list(), list(), list()
    is_first_line = True
    for raw_line in in_file:
        line = raw_line.strip()
        id_str, go_str1, go_str2 = line.split(sep, maxsplit=3)[0:3]
        for go_str, go_list in zip([go_str1, go_str2], [go_list1, go_list2]):
            go_sublist = [go.strip() for go in go_str.upper().split(go_sep) if go.strip() != ""]
            go_list.append(go_sublist)
        if is_first_line:
            is_first_line = False
            if not any(map(is_go_term, go_list1[0] + go_list2[0])):
                logging.info(f"first line looks like header, skipping: {raw_line}")
                go_list1, go_list2 = list(), list()
                continue
        id_list.append(id_str.strip())
    return id_list, go_list1, go_list2


def get_frequency(go_id, termcounts, godag):
    go_term = godag[go_id]
    namespace = go_term.namespace
    if (namespace == 'molecular_function'):
        parent_count = termcounts.get('GO:0003674')
    elif (namespace == 'cellular_component'):
        parent_count = termcounts.get("GO:0005575")
    else:
        parent_count = termcounts.get('GO:0008150')

    return float(termcounts.get(go_id, 0)) / parent_count

def get_ic(go_id,termcounts,godag):
    freq = get_frequency(go_id,termcounts,godag)
    if(freq == 0):
        return 0
    return 0.0 - math.log(freq)


def BMA(GO_list1, GO_list2, termcounts, godag, similarity_method=None):
    summationSet12 = 0.0
    summationSet21 = 0.0
    for id1 in GO_list1:
        similarity_values = []
        for id2 in GO_list2:
            similarity_values.append(Rel_Metric(id1, id2, godag, termcounts))
        summationSet12 += max(similarity_values + [-1])
    for id2 in GO_list2:
        similarity_values = []
        for id1 in GO_list1:
            similarity_values.append(Rel_Metric(id2, id1, godag, termcounts))
        summationSet21 += max(similarity_values + [-1])
    return (summationSet12 + summationSet21) / (len(GO_list1) + len(GO_list2))


def get_highest_ic_anc(id, termcounts, godag):
    if termcounts.get(id, 0) > 0:
        return 0
    gosubdag_r0 = GoSubDag([id], godag, prt=None)
    P = gosubdag_r0.rcntobj.go2parents[id]
    max_ic = 0
    for i in P:
        ic = get_ic(i, termcounts,godag)
        if (max_ic < ic):
            max_ic = ic
    return max_ic


def Rel_Metric(id1, id2, godag, termcounts):
    if id1 not in godag or id2 not in godag:
        return -1

    goterm1 = godag[id1]
    goterm2 = godag[id2]
    if goterm1.namespace == goterm2.namespace:
        mica_goid = deepest_common_ancestor([id1, id2], godag)
        freq = get_frequency(mica_goid, termcounts,godag)
        info_content = get_ic(mica_goid, termcounts,godag)
        info_content1 = get_ic(id1, termcounts,godag)
        info_content2 = get_ic(id2, termcounts,godag)
        if info_content1 == 0:
            info_content1 = get_highest_ic_anc(id1, termcounts,godag)
        if (info_content2 == 0):
            info_content2 = get_highest_ic_anc(id2, termcounts,godag)
        if info_content1 + info_content2 == 0:
            return 0
        return (2 * info_content * (1 - freq)) / (info_content1 + info_content2)
    else:    # if goterms are from different GO namespaces (molecular function, cellular component, biological process)
        return -1


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Calculate semantic distance for sets of Gene Ontology terms'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
                        metavar='LOG_FILE',
                        type=str,
                        help='record program progress in LOG_FILE')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--plot', dest="plot_file",
                        help="Draw swarm plot of calculated similarities. Filetype is automatically determined based on"
                             " extension (e.g. .png, .svg)",
                        default=None
                        )
    parser.add_argument('input_table',
                        metavar='INPUT_TABLE',
                        nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='Input table file')
    return parser.parse_args()


class LogFile(object):
    """File-like object to log text using the `logging` module."""

    def __init__(self):
        self.logger = logging.getLogger()

    def write(self, msg, level=logging.DEBUG):
        msg = msg.strip("\n")
        self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()


class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


def run_process(ids, go1, go2, freq_dict, queue, godag=None):
    if godag is None:
        godag = GODag(GODAG_FILE_PATH, prt=LogFile())
    for id in ids:
        BMA_test = BMA(go1[id], go2[id], freq_dict, godag)
        queue.put([id, BMA_test])


def run_comparison(in_file):
    start = time.time()
    ids, GO_list1, GO_list2 = read_input(in_file)

    if not os.path.isfile(JSON_INDEXED_FILE_PATH):
        make_GO_freq_json.intialize_termcounts()

    freq_dict = json.load(open(JSON_INDEXED_FILE_PATH))

    end = time.time()
    logging.debug(f"Resource loading took {round(end - start, 2)} s")

    start = time.time()
    queue = multiprocessing.Queue()
    jobs = []

    cores = multiprocessing.cpu_count()
    logging.debug(f"Started comparison with {cores} cores / cpu's.")

    if platform.system() == "Linux":
        godag = GODag(GODAG_FILE_PATH, prt=LogFile())

    numeric_ids = range(0, len(GO_list1))
    portion_per_core = len(GO_list1) // cores
    for core in range(cores):
        logging.debug(f"Started process {core}.")
        if core == cores - 1:
            current_ids = numeric_ids[core * portion_per_core:]
        else:
            current_ids = numeric_ids[core * portion_per_core:(core + 1) * portion_per_core]

        if len(current_ids) > 0:
            if platform.system() == "Linux":
                p = multiprocessing.Process(target=run_process, args=(current_ids, GO_list1, GO_list2, freq_dict, queue, godag))
            else:
                p = multiprocessing.Process(target=run_process, args=(current_ids, GO_list1, GO_list2, freq_dict, queue))
            jobs.append(p)
            p.start()

    for job in jobs:
        job.join()

    return_dict = dict()
    while not queue.empty():
        id, sim = queue.get()
        return_dict[id] = sim

    end = time.time()
    logging.debug(f"Similarity calculation took {round(end - start, 2)} s")

    print(HEADER)
    csv_string = HEADER
    for i, id in enumerate(ids):
        line = f"{id},{return_dict[i]}"
        print(line)
        csv_string += "\n" + line
    return csv_string


def plot_similarity(list_similarity_values):
    l_is_number = [isinstance(x, numbers.Number) for x in list_similarity_values]
    if not all(l_is_number):
        raise ValueError(f"List contains non numeric values: {list_similarity_values}")
    ax = sns.swarmplot(x=list_similarity_values)
    fig = ax.get_figure()
    return fig


def process_file(options):
    if options.input_table == sys.stdin:
        logging.info("Processing input table file from stdin")
    else:
        logging.info("Processing input table file from %s", options.input_table.name)

    csv_table_string = run_comparison(options.input_table)
    list_similarity_values = []
    for l in csv_table_string.split("\n")[1:]:
        list_similarity_values.append(float(l.split(",")[1]))
    if options.plot_file:
        figure = plot_similarity(list_similarity_values)
        figure.savefig(options.plot_file)


def init_logging(log_filename, verbose):
    """Initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: string name of the log file to write to
          or None, if is None, log output will go tto stderr
        verbose: integer, increase verbosity level. Default
        level is WARNING, 1->INFO, 2->DEBUG, >=3->NOTSET
    Result:
        None
    """
    verbosity = 30 - verbose * 10
    if verbosity < 0:
        verbosity = 0

    args = {"level": verbosity,
            "filemode": 'w',
            "format": '%(asctime)s %(levelname)s - %(message)s',
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"}

    if log_filename is None:
        args["stream"] = sys.stderr
    else:
        args["filename"] = log_filename

    logging.basicConfig(**args)
    logging.info('program started')
    logging.info('command line: %s', ' '.join(sys.argv))


def main():
    options = parse_args()
    init_logging(options.log, options.verbose)
    process_file(options)
    logging.info("Done!")


if __name__ == "__main__":
    main()
