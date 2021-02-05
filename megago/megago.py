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

from goatools.obo_parser import GODag
from progress.bar import IncrementalBar

from .constants import GO_DAG_FILE_PATH
from .precompute_highest_ic import get_highest_ic
from .metrics import compute_bma_metric
from .precompute_frequency_counts import get_frequency_counts
from .heatmap import generate_heatmap



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
    parser.add_argument('--heatmap',
                        action='store_true',
                        help="Generate an interactive heatmap for the compared samples")
    parser.add_argument('samples',
                        metavar='SAMPLES',
                        nargs=argparse.REMAINDER,
                        type=str,
                        help='Samples that should be compared to each other')

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


def get_default_go_dag():
    return GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))


def run_comparison(go_list_1, go_list_2, go_dag=None, progress=None):
    """ Compute the pairwise similarity values for all rows from the given file.

    Parameters
    ----------
    go_list_1 : a list with GO-identifiers as strings
        All GO-terms present in the first sample.
    go_list_2 : a list with GO-identifiers as strings
        All GO-terms present in the second sample.
    go_dag : GODag object
        GODag object from the goatools package
    progress : function (number) => void
        is called with the current progress value (a floating point value between 0 and 1)

    Returns
    -------
    tuple
        A tuple with 3 values. These correspond to the similarity scores of biological process, cellular component and
        molecular function respectively.
    """

    freq_dict = get_frequency_counts()
    highest_ic_anc = get_highest_ic()
    if go_dag is None:
        go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))

    split_per_domain_1 = split_per_domain(go_list_1, go_dag)
    split_per_domain_2 = split_per_domain(go_list_2, go_dag)

    output = list()

    total_comparisons = len(set(go_list_1)) * len(set(go_list_2))
    done = 0

    def progress_reporter(batch_size):
        nonlocal done
        if progress:
            done += batch_size
            progress(done / total_comparisons)

    for i in range(len(GO_DOMAINS)):
        output.append(
            compute_bma_metric(
                split_per_domain_1[i],
                split_per_domain_2[i],
                freq_dict,
                highest_ic_anc,
                progress_reporter,
                similarity_method="lin"
            )
        )

    if progress:
        progress(1)

    return tuple(output)


def find_non_existing_terms(go_list, go_dag):
    """ Checks if each of the given terms from the go_list are present in the GO-dag. Returns a list with all terms that
    are not present.

    Parameters
    ----------
    go_list : a list with GO-identifiers as strings.
        Every identifier is looked up in the go_dag and is added to the output if it does not exist.
    go_dag: A valid GO graph.

    Returns
    -------
    set
        A set with all GO-identifiers from the go_list that are not present in the given go_dag.
    """
    return set(x for x in go_list if not is_go_term(x) or x not in go_dag)


def plot_similarity(list_similarity_values):
    l_is_number = [isinstance(x, numbers.Number) for x in list_similarity_values]
    if not all(l_is_number):
        raise ValueError(f"List contains non numeric values: {list_similarity_values}")
    ax = sns.swarmplot(x=list_similarity_values)
    fig = ax.get_figure()
    return fig


def process(options):
    samples = []
    sample_names = []

    for sample in options.samples:
        # The GO-terms that need to be compared can be given as a CSV-file or inline in the command as a ";" delimited
        # string.
        if re.match(".*\.[^.]+$", sample):
            logging.info("Processing sample 1 from %s", sample)
            sample_names.append(sample)
            samples.append(read_input(open(sample, 'r')))
        else:
            samples.append(sample.split(';'))

    all_results = {}

    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            results = run_comparison(samples[i], samples[j])
            all_results[(i, j)] = results

            print(f"Results for sample {i} and {j}")
            print(HEADER)
            lines = [HEADER]
            for idx, domain in enumerate(GO_DOMAINS):
                line = f"{domain},{results[idx]}"
                print(line)
                lines.append(line)

            csv_table_string = "\n".join(lines)
            list_similarity_values = []
            for l in csv_table_string.split("\n")[1:]:
                list_similarity_values.append(float(l.split(",")[1]))
            if options.plot_file:
                figure = plot_similarity(list_similarity_values)
                figure.savefig(options.plot_file)

    if options.heatmap:
        generate_heatmap(all_results, sample_names if len(sample_names) == len(samples) else ["Sample " + str(i) for i in range(len(samples))])



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
    logging.info(f"MegaGO version {PROGRAM_VERSION}")
    process(options)
    logging.info("Done!")


if __name__ == "__main__":
    main()
