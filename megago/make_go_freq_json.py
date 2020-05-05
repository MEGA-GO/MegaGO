import json
from goatools.anno.idtogos_reader import IdToGosReader
from goatools.obo_parser import GODag
from goatools.semantic import TermCounts
import os
from . import DATA_DIR, JSON_INDEXED_FILE_PATH, uniprot_time_stamp, UNIPROT_ASSOCIATIONS_FILE_PATH


def intialize_termcounts():
    go_freq_dict = dict()
    godag = GODag(os.path.join(DATA_DIR,"go-basic.obo"))

    associations = IdToGosReader(UNIPROT_ASSOCIATIONS_FILE_PATH, godag=godag).get_id2gos('all')
    termcounts = TermCounts(godag, associations)
    for i in godag.values():
        go_freq_dict[i.id] = termcounts.get_count(i.id)
    go_freq_dict['db_date'] = uniprot_time_stamp
    # write frequency dict to JSON file
    with open(JSON_INDEXED_FILE_PATH, 'w') as json_file:
        json.dump(go_freq_dict, json_file)
