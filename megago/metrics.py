import math

from goatools.semantic import deepest_common_ancestor
from goatools.gosubdag.gosubdag import GoSubDag

from .constants import NAN_VALUE

deepest_common_ancestor_cache = dict()


def get_frequency(go_id, term_counts, go_dag):
    go_term = go_dag[go_id]
    namespace = go_term.namespace
    if namespace == 'molecular_function':
        parent_count = term_counts.get('GO:0003674')
    elif namespace == 'cellular_component':
        parent_count = term_counts.get("GO:0005575")
    else:
        parent_count = term_counts.get('GO:0008150')

    return float(term_counts.get(go_id, 0)) / parent_count


def get_ic(go_id, term_counts, go_dag):
    freq = get_frequency(go_id, term_counts, go_dag)
    if freq == 0:
        return 0
    return 0.0 - math.log(freq)


def get_highest_ic_anc(id, term_counts, go_dag):
    if term_counts.get(id, 0) > 0:
        return 0
    gosubdag_r0 = GoSubDag([id], go_dag, prt=None)
    if id in gosubdag_r0.rcntobj.go2ancestors:
        P = gosubdag_r0.rcntobj.go2ancestors[id]
        max_ic = 0
        for i in P:
            ic = get_ic(i, term_counts, go_dag)
            if max_ic < ic:
                max_ic = ic
        return max_ic
    else:
        return 0


def get_deepest_common_ancestor(id1, id2, go_dag):
    global deepest_common_ancestor_cache
    key = (id1, id2) if id1 < id2 else (id2, id1)
    if key not in deepest_common_ancestor_cache:
        deepest_common_ancestor_cache[key] = deepest_common_ancestor([id1, id2], go_dag)
    return deepest_common_ancestor_cache[key]


def rel_metric(id1, id2, go_dag, term_counts, highest_ic_anc):
    """
    Computes the relative metric between the GO-terms id1 and id2.
    :param id1: string representation of the first GO-term that will be compared with id2.
    :param id2: string representation of the second GO-term that will be compared with id1.
    :param go_dag: A Direct Acyclic Graph of all GO-terms.
    :param term_counts: A dictionary that maps each GO-term onto it's frequency.
    :param highest_ic_anc: A dictionary that maps each GO-term onto it's highest information content of all ancestors.
    :return: A floating point value (a score) that indicates how similar the GO-terms id1 and id2 are.
    """
    if (id1 not in go_dag) or (id2 not in go_dag):
        return NAN_VALUE

    go_term1 = go_dag[id1]
    go_term2 = go_dag[id2]
    if go_term1.namespace == go_term2.namespace:
        mica_goid = get_deepest_common_ancestor(id1, id2, go_dag)
        freq = get_frequency(mica_goid, term_counts, go_dag)
        info_content = get_ic(mica_goid, term_counts, go_dag)
        info_content1 = get_ic(id1, term_counts, go_dag)
        info_content2 = get_ic(id2, term_counts, go_dag)
        if info_content1 == 0:
            info_content1 = highest_ic_anc[id1]
        if info_content2 == 0:
            info_content2 = highest_ic_anc[id2]
        if info_content1 + info_content2 == 0:
            return 0
        return (2 * info_content * (1 - freq)) / (info_content1 + info_content2)
    else:    # if goterms are from different GO namespaces (molecular function, cellular component, biological process)
        return NAN_VALUE


def compute_bma_metric(go_list1, go_list2, term_counts, go_dag, highest_ic_anc, similarity_method=rel_metric):
    summation_set12 = 0.0
    summation_set21 = 0.0
    for id1 in go_list1:
        similarity_values = []
        for id2 in go_list2:
            similarity_values.append(similarity_method(id1, id2, go_dag, term_counts, highest_ic_anc))
        summation_set12 += max(similarity_values + [NAN_VALUE])
    for id2 in go_list2:
        similarity_values = []
        for id1 in go_list1:
            similarity_values.append(similarity_method(id2, id1, go_dag, term_counts, highest_ic_anc))
        summation_set21 += max(similarity_values + [NAN_VALUE])
    return (summation_set12 + summation_set21) / (len(go_list1) + len(go_list2))
