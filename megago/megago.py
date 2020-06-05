"""Mega-GO - Calculate semantic distance for sets of Gene Ontology (GO) terms.

Read a file that contains GO terms and print their semantic similarity.
"""

import argparse
import numbers
import seaborn as sns
import sys
import logging
import pkg_resources
import re
import os
import concurrent.futures

from goatools.obo_parser import GODag

from .constants import GO_DAG_FILE_PATH
from .precompute_highest_ic import get_highest_ic
from .metrics import compute_bma_metric
from .precompute_frequency_counts import get_frequency_counts


EXIT_COMMAND_LINE_ERROR = 2
EXIT_FASTA_FILE_ERROR = 3
DEFAULT_MIN_LEN = 0
DEFAULT_VERBOSE = False
HEADER = 'DOMAIN,SIMILARITY'
PROGRAM_NAME = "megago"
GO_DOMAINS = [
    "biological_process",
    "cellular_component",
    "molecular_function"
]
# How many items should be present in a sample before we compute metrics in parallel?
PARALLEL_TRESHOLD = 200

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def is_go_term(candidate):
    """ Returns true if a given string could be a valid GO-term identifier. This function only checks if the string
    satisfies the formatting of a GO-term identifier, not if it actually exists in the ontology!

    Parameters
    ----------
    candidate : str
        A string for which we should verify if it's a valid GO-identifier.

    Returns
    -------
    bool
    """
    regex = re.compile(r"^go:\d{7}$", re.IGNORECASE)
    return bool(regex.match(candidate))


def read_input(in_file, header=True):
    """Read and return all GO terms that are found in an open file.

    Parameters
    ----------
    in_file : an open file object
    header : bool, optional
        If the file contains a header that should be stripped

    Returns
    -------
    A list with all GO-term id's that are present in the given file.

    """
    if header:
        next(in_file)
    return [line.rstrip() for line in in_file]


def parse_args():
    """ Parse command line arguments. This function will exit the program on a command line error!

    Returns
    -------
    Options object with command line argument values as attributes.
    """
    parser = argparse.ArgumentParser(description=__doc__)

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
    parser.add_argument('sample_1',
                        metavar='SAMPLE_1',
                        nargs='?',
                        type=str,
                        help='Input file for sample 1')
    parser.add_argument('sample_2',
                        metavar='SAMPLE_2',
                        nargs='?',
                        type=str,
                        help='Input file for sample 2')

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


def split_per_domain(go_terms, go_dag):
    """ Split a list of go_terms into three different lists that correspond to the GO-domains.

    Parameters
    ----------
    go_terms : a list of strings
        a list of GO terms that need to be divided over the different GO-domains.
    go_dag : a graph that represents the Gene Ontology

    Returns
    -------
    biological_process, cellular_component, molecular_function
        Three different lists with respectively the GO-terms that belong to the biological process, cellular component
        and molecular function domains.
    """
    output = {domain: [] for domain in GO_DOMAINS}

    for go_term in go_terms:
        if go_term in go_dag:
            ns = go_dag[go_term].namespace
            output[ns].append(go_term)
        else:
            logging.warning(f"{go_term} was not found in the Gene Ontology parsed by this script.")

    return [output[domain] for domain in GO_DOMAINS]


def run_comparison(go_list_1, go_list_2):
    """ Compute the pairwise similarity values for all rows from the given file.

    Parameters
    ----------
    go_list_1 : a list with GO-identifiers as strings
        All GO-terms present in the first sample.
    go_list_2 : a list with GO-identifiers as strings
        All GO-terms present in the second sample.

    Returns
    -------
    str
        A string that represents a "CSV"-file with a similarity value per row.
    """

    freq_dict = get_frequency_counts()
    highest_ic_anc = get_highest_ic()
    go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))

    split_per_domain_1 = split_per_domain(go_list_1, go_dag)
    split_per_domain_2 = split_per_domain(go_list_2, go_dag)

    results = [
        compute_bma_metric(
            split_per_domain_1[i],
            split_per_domain_2[i],
            freq_dict,
            go_dag,
            highest_ic_anc
        ) for i in range(len(GO_DOMAINS))
    ]

    print(HEADER)
    lines = [HEADER]
    for idx, domain in enumerate(GO_DOMAINS):
        line = f"{domain},{results[idx]}"
        print(line)
        lines.append(line)
    return "\n".join(lines)


def plot_similarity(list_similarity_values):
    l_is_number = [isinstance(x, numbers.Number) for x in list_similarity_values]
    if not all(l_is_number):
        raise ValueError(f"List contains non numeric values: {list_similarity_values}")
    ax = sns.swarmplot(x=list_similarity_values)
    fig = ax.get_figure()
    return fig


def process(options):
    # The GO-terms that need to be compared can be given as a CSV-file or inline in the command as a ";" delimited
    # string.
    if options.sample_1.endswith('.csv'):
        logging.info("Processing sample 1 from %s", options.sample_1)
        go_list_1 = read_input(open(options.sample_1, 'r'))
    else:
        go_list_1 = options.sample_1.split(';')

    if options.sample_2.endswith('.csv'):
        logging.info("Processing sample 2 from %s", options.sample_2)
        go_list_2 = read_input(open(options.sample_2, 'r'))
    else:
        go_list_2 = options.sample_2.split(';')

    csv_table_string = run_comparison(go_list_1, go_list_2)
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

    Parameters
    ----------
    log_filename : str
        name of the log file to write to or None, if is None, log output will go tto stderr
    verbose : int
        increase verbosity level. (default is WARNING, 1->INFO, 2->DEBUG, >=3->NOTSET)

    Returns
    -------
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
    process(options)
    logging.info("Done!")


if __name__ == "__main__":
    main()
