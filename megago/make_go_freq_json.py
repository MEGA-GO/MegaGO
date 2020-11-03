import json
from goatools.anno.idtogos_reader import IdToGosReader
from goatools.obo_parser import GODag
from goatools.semantic import TermCounts
import os
from . import DATA_DIR, JSON_INDEXED_FILE_PATH, UNIPROT_ASSOCIATIONS_FILE_PATH


def intialize_term_counts():
    go_freq_dict = dict()
    go_dag = GODag(os.path.join(DATA_DIR, "go-basic.obo"))

    associations = IdToGosReader(UNIPROT_ASSOCIATIONS_FILE_PATH, godag=go_dag).get_id2gos('all')
    term_counts = TermCounts(go_dag, associations)
    for i in go_dag.values():
        go_freq_dict[i.id] = term_counts.get_count(i.id)
    # write frequency dict to JSON file
    with open(JSON_INDEXED_FILE_PATH, 'w') as json_file:
        json.dump(go_freq_dict, json_file)
