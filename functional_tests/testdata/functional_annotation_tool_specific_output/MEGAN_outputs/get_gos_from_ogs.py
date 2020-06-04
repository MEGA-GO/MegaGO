import requests
import json

f = open("737NSvsWS_EGGNOGcount.csv", 'r')

# remove header line
f.readline()

ogs = []
for line in f:
    ogs.append(line.strip('\n').split()[0])

# # request json from eggNOG api
def get_gos(ogs):
    with open('go_terms.txt', 'w') as outfile:
        outfile.write('og' + '\t' + 'gos' + '\n')
        for i in range(len(ogs)):
            grp = ogs[i]
            url = 'http://eggnogapi.embl.de/nog_data/json/go_terms/' + grp
            print("Retrieving " + url)
            response = requests.get(url)
            if response.status_code != 200:
                go_to_write = "failed_request"
            else:
                top_dict = response.json()['go_terms']
                # may not have any go terms
                go_lists = [top_dict[k] for k in top_dict.keys()]
                if len(go_lists) > 0:
                    go_list2 = []
                    for go_list in go_lists:
                        go_list2 += go_list
                    go_to_write = ','.join([entry[0] for entry in go_list2])
                else:
                    go_to_write = "NA"
            outfile.write(ogs[i] + "\t" + go_to_write + "\n")

go_terms = get_gos(ogs)


