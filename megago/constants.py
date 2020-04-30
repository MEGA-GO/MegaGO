import pkg_resources
import os

# Main directory that contains all resources for this module.
DATA_DIR = pkg_resources.resource_filename(__name__, 'resources')

# File that contains the precomputed frequency counts.
FREQUENCY_COUNTS_FILE_PATH = os.path.join(DATA_DIR, "frequency_counts_uniprot.json")

# Serialized version of the Direct Acyclic Graph of all GO-terms. Can be downloaded from
# http://geneontology.org/docs/download-ontology/
GO_DAG_FILE_PATH = os.path.join(DATA_DIR, "go-basic.obo")

# File that contains the UniProt associations at a specific moment in time (SwissProt)
UNIPROT_ASSOCIATIONS_FILE_PATH = os.path.join(DATA_DIR, "associations-uniprot-sp-20200116.tab")

# Timestamp of the downloaded UniProt associations. This timestamp is used to determine if the frequency counts
# and information content needs to be updated.
UNIPROT_TIME_STAMP = ((UNIPROT_ASSOCIATIONS_FILE_PATH.split('-')[-1]).split('.'))[0]

# File that contains the precomputed information content values
HIGHEST_IC_FILE_PATH = os.path.join(DATA_DIR, "highest_ic_uniprot.json")

NAN_VALUE = float('nan')
