import argparse
import numbers
import seaborn as sns
import sys
import logging
import pkg_resources
import re
import os

from goatools.obo_parser import GODag

from .constants import GO_DAG_FILE_PATH
from .precompute_highest_ic import get_highest_ic
from .metrics import compute_bma_metric
from .precompute_frequency_counts import get_frequency_counts


EXIT_COMMAND_LINE_ERROR = 2
EXIT_FASTA_FILE_ERROR = 3
DEFAULT_MIN_LEN = 0
DEFAULT_VERBOSE = False
HEADER = 'ID,SIMILARITY'
PROGRAM_NAME = "megago"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def is_go_term(candidate):
    """
    Checks if a given string could be a valid GO-term identifier. This function only checks if the string satisfies the
    formatting of a GO-term identifier, not if it actually exists in the ontology!
    :param candidate: A string for which we should verify if it's a valid GO-identifier.
    :return: True if the string is indeed a valid identifier, False otherwise.
    """
    regex = re.compile(r"^go:\d{7}$", re.IGNORECASE)
    return regex.match(candidate)


def read_input(in_file, sep=",", go_sep=";"):
    """
    Read a csv with three columns: ID, GO terms 1, GO terms 2, coming from two datasets
    :param in_file: an open file object
    :param sep: field separator of input file, default: ','
    :param go_sep: separator between individual go terms, default: ';'
    :return: id_list and two nested lists of GO terms
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


def parse_args():
    """
    Parse command line arguments. This function will exit the program on a command line error!
    :return: Options object with command line argument values as attributes.
    """
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


def run_comparison(in_file):
    """
    Compute the pairwise similarity values for all rows from the given file.
    :param in_file: The file for wich row-wise similarities should be computed.
    :return: A string that represents a "CSV"-file with a similarity value per row.
    """

    # These are lists of lists with GO-terms. Both outer lists contain the same number of elements
    ids, go_lists1, go_lists2 = read_input(in_file)
    freq_dict = get_frequency_counts()
    highest_ic_anc = get_highest_ic()
    go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))

    values = []

    for i in range(len(go_lists1)):
        go_list1 = go_lists1[i]
        go_list2 = go_lists2[i]
        values.append(compute_bma_metric(go_list1, go_list2, freq_dict, go_dag, highest_ic_anc))

    print(HEADER)
    lines = [HEADER]
    for idx, val in enumerate(values):
        line = f"{ids[idx]},{val}"
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
