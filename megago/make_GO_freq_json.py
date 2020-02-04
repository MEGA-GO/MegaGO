import json

"""
Given UniProt input file "uniprot-reviewed_yes.tab", 
create nicely intermediate formatted file "uniprot-sp.tab",
create JSON file with GO frequencies UniProt/SwissProt.
"""

uniprot_download = "uniprot-reviewed_yes.tab"  # default name
uniprot_formatted = "uniprot-sp.tab"

# format the downloaded uniprot file to uniform template
with open(uniprot_download, "r") as in_f, open(uniprot_formatted, "w") as out_f:
    print(in_f.readline().rstrip(), file=out_f)
    for line in in_f:
        try:
            entry, go_terms= line.rstrip().split("\t", maxsplit=1)
            go_terms = go_terms.replace(" " ,"") + ";"
        except ValueError:
            entry = line.rstrip()
            go_terms = ""
        print(entry + "\t" + go_terms, file=out_f)


# create dict for go_terms
go_freq_dict = dict()

"""
# calculate sha256 checksum of uniprot_file  # a bit overkill?
import hashlib
sha256_hash = hashlib.sha256()
with open(uniprot_formatted, "rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(byte_block)
    go_freq_dict["sha256"] = sha256_hash.hexdigest()
"""

# calculate frequencies of each GO term
with open(uniprot_formatted, "r") as f:
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