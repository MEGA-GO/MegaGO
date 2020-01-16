from goatools.obo_parser import GODag
import os
from goatools.associations import dnld_assc
from goatools.semantic import deepest_common_ancestor
from goatools.semantic import semantic_similarity
from goatools.semantic import TermCounts, get_info_content
from goatools.semantic import lin_sim



godag = GODag("go-basic.obo")
fin_gaf = os.path.join(os.getcwd(), "tair.gaf")
associations = dnld_assc(fin_gaf, godag)

go_id3 = 'GO:0048364'
go_id4 = 'GO:0032501'

go_root = deepest_common_ancestor([go_id3, go_id4], godag)

sim = semantic_similarity(go_id3, go_id4, godag)
print('The semantic similarity between terms {} and {} is {}.'.format(go_id3, go_id4, sim))

# First get the counts of each GO term.
termcounts = TermCounts(godag, associations)

# Calculate the information content
go_id = "GO:0008152"
infocontent = get_info_content(go_id, termcounts)
print('Information content ({}) = {}'.format(go_id, infocontent))


sim_l = lin_sim(go_id3, go_id4, godag, termcounts)
print('Lin similarity score ({}, {}) = {}'.format(go_id3, go_id4, sim_l))

freq = termcounts.get_term_freq(go_id)

def BMA(set1,set2,similarity_method):
    summationSet12 = 0.0
    summationSet21 = 0.0
    for id1 in set1:
        similarity_values = []
        for id2 in set2:
            similarity_values.append(Rel_Metric(id1,id2,godag,termcounts))
        summationSet12 += max(similarity_values)
    for id2 in set2:
        similarity_values = []
        for id1 in set1:
            similarity_values.append(Rel_Metric(id2,id1,godag,termcounts))
        summationSet21 += max(similarity_values)
    return (summationSet12+summationSet21)/(len(set1)+len(set2))

def Rel_Metric(id1,id2,godag,termcounts):
    mica_goid = deepest_common_ancestor([go_id1, go_id2], godag)
    freq = termcounts.get_term_freq(mica_goid) 
    infocontentMica = get_info_content(mica_goid, termcounts)
    infocontent1 = get_info_content(go_id1, termcounts)
    infocontent2 = get_info_content(go_id2, termcounts)

    return (2*infocontent*(1-freq))/(infocontent1+infocontent2)
