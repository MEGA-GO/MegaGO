import pkg_resources
import os

DATA_DIR = pkg_resources.resource_filename(__name__, 'resource_data')
JSON_INDEXED_FILE_PATH = os.path.join(DATA_DIR, "go_freq_uniprot.json")
UNIPROT_ASSOCIATIONS_FILE_PATH = os.path.join(DATA_DIR, "associations-uniprot-sp-20200116.tab")
uniprot_time_stamp = ((UNIPROT_ASSOCIATIONS_FILE_PATH.split('-')[-1]).split('.'))[0]
NAN_VALUE = float('nan')
