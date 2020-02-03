import json
import hashlib

"""
Given Uniprot input file, calculate sha256 checksum, put GO frequencies in JSON.
"""


uniprot_file = "uniprot-sp.tab"
go_freq_dict = dict()

# calculate sha256 checksum of uniprot_file
sha256_hash = hashlib.sha256()
with open(uniprot_file, "rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(byte_block)
    go_freq_dict["sha256"] = sha256_hash.hexdigest()

# calculate frequencies of each GO term
with open(uniprot_file, "r") as f:
    next(f)
    for line in f:
        try:
            gos = line.rstrip().split("\t", maxsplit=1)[1]
            for go in gos.split(';')[:-1]:  # except empty value after last semicolon
                if go not in go_freq_dict.keys():
                    go_freq_dict[go] = 1
                else:
                    go_freq_dict[go] += 1

        except IndexError:  # no GO term assigned to protein
            pass

# write frequency dict to JSON file
with open('go_freq_uniprot.json', 'w') as json_file:
    json.dump(go_freq_dict, json_file)

