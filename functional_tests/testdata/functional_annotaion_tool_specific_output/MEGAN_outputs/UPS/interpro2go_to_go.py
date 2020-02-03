import urllib.request
import re
import xlrd

# Writes GO terms to go_terms.txt output alongside the interproteins
def interpro2GO(interproteins):
    response = urllib.request.urlopen('http://current.geneontology.org/ontology/external2go/interpro2go')
    i2go_map = response.read().decode('utf-8').split('\n')
    go_regex = re.compile('GO:\d{7}')
    with open('go_terms.txt', 'w') as outfile:
        outfile.write('interpro2go' + '\t' + 'go' + '\n')
        for prot in interproteins:
            GO_terms = [];
            for line in i2go_map:
                if prot in line:
                    GO_terms.append(go_regex.search(line)[0])
            outfile.write(prot + '\t' + ','.join(GO_terms) + '\n')

def extractProteins(filename):
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    interproteins = []
    for row in range(worksheet.nrows):
        value = worksheet.cell_value(row, 1).replace('"','').strip()
        if value != "No hits":
            interproteins.append(value)
    return interproteins

all_proteins = extractProteins('UPS1_03_reads to IP2G.xlsx') + extractProteins('UPS2_03_reads to IP2G.xlsx')
unique_proteins = set(all_proteins)

interpro2GO(unique_proteins)
