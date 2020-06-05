import math

from goatools.semantic import deepest_common_ancestor
from goatools.gosubdag.gosubdag import GoSubDag

from .constants import NAN_VALUE

deepest_common_ancestor_cache = dict()
rel_metric_cache = dict()


def get_frequency(go_id, term_counts, go_dag):
    """get the relative frequency of go_id in it's respective namespace.

    The number of occurrences of the provided go_id and all of its children is divided by the total number of term
    occurrences in the associated GO namespace.

    Parameters
    ----------
    go_id : str
        gene ontology ID that the relative frequency should be calculated for
    term_counts : dict
        dictionary: key: GO terms, values: number of occurrences of GO term and its children in body of evidence
    go_dag : GODag object
        GODag object from the goatools package

    Returns
    -------
    float
    """
    go_term = go_dag[go_id]
    namespace = go_term.namespace
    if namespace == 'molecular_function':
        parent_count = term_counts.get('GO:0003674')
    elif namespace == 'cellular_component':
        parent_count = term_counts.get("GO:0005575")
    else:
        parent_count = term_counts.get('GO:0008150')

    return float(term_counts.get(go_id, 0)) / parent_count


def get_info_content(go_id, term_counts, go_dag):
    """get information content of go_id

    The information content is calculated as negative natural logarithm of the relative frequency of go_id.

    Parameters
    ----------
    go_id : str
        gene ontology ID that the relative frequency should be calculated for
    term_counts : dict
        dictionary: key: GO terms, values: number of occurrences of GO term and its children in body of evidence
    go_dag : GODag object
        GODag object from the goatools package

    Returns
    -------
    float
        if relative frequency of go_id == 0: 0
        else: negative natural logarithm of the relative frequency of go_id

    """
    freq = get_frequency(go_id, term_counts, go_dag)
    if freq == 0:
        return 0
    return 0.0 - math.log(freq)


def get_ic_of_most_informative_ancestor(id, term_counts, go_dag):
    """get the information content of the go_id parent with the highest information content.

    Parameters
    ----------
    go_id : str
        GO term
    term_counts : dict
        dictionary: key: GO terms, values: number of occurrences of GO term and its children in body of evidence
    go_dag : GODag object
        GODag object from the goatools package


    Returns
    -------
    float

    """
    if term_counts.get(id, 0) > 0:
        return 0
    gosubdag_r0 = GoSubDag([id], go_dag, prt=None)
    if id in gosubdag_r0.rcntobj.go2ancestors:
        P = gosubdag_r0.rcntobj.go2ancestors[id]
        max_ic = 0
        for i in P:
            ic = get_info_content(i, term_counts, go_dag)
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


def rel_metric(go_id1, go_id2, go_dag, term_counts, highest_ic_anc):
    """calculate semantic similarity of the GO terms id1 and id2 using the rel metric

    Formula of the metric: (2 * info_content(mica) * (1 - freq(mica))) / (info_content(go_id1) + info_content(go_id2))
    where mica is the most informative common ancestor of go_id1 and go_id2.
    Metric is implemented according to: Schlicker, A., Domingues, F.S., Rahnenführer, J. et al. A new measure for
    functional similarity of gene products based on Gene Ontology. BMC Bioinformatics 7, 302 (2006)
    doi:10.1186/1471-2105-7-302


    Parameters
    ----------
    go_id1 : str
        GO term
    go_id2 : str
        GO term
    go_dag : GODag object
        GODag object from the goatools package
    term_counts : dict
        dictionary: key: GO terms, values: number of occurrences of GO term and its children in body of evidence

    Returns
    -------
    float
        if go_id1 and go_id2 are from different GO namespaces or either of them misses in the go_dag: NAN_VALUE
        else: rel metric

    """
    global rel_metric_cache

    key = (go_id1, go_id2) if go_id1 < go_id2 else (go_id2, go_id1)
    if key in rel_metric_cache:
        return rel_metric_cache[key]

    if (go_id1 not in go_dag) or (go_id2 not in go_dag):
        return NAN_VALUE

    go_term1 = go_dag[go_id1]
    go_term2 = go_dag[go_id2]
    if go_term1.namespace == go_term2.namespace:
        mica_goid = get_deepest_common_ancestor(go_id1, go_id2, go_dag)
        freq = get_frequency(mica_goid, term_counts, go_dag)
        info_content = get_info_content(mica_goid, term_counts, go_dag)
        info_content1 = get_info_content(go_id1, term_counts, go_dag)
        info_content2 = get_info_content(go_id2, term_counts, go_dag)
        if info_content1 == 0:
            info_content1 = highest_ic_anc[go_id1]
        if info_content2 == 0:
            info_content2 = highest_ic_anc[go_id2]
        if info_content1 + info_content2 == 0:
            return 0
        result = (2 * info_content * (1 - freq)) / (info_content1 + info_content2)
    else:    # if goterms are from different GO namespaces (molecular function, cellular component, biological process)
        result = NAN_VALUE
    rel_metric_cache[key] = result
    return result


def _do_compute_max_sim_value(go_list1, go_list2, go_dag, term_counts, highest_ic_anc, similarity_method=rel_metric):
    for id1 in go_list1:
        similarity_values = []
        for id2 in go_list2:
            similarity_values.append(similarity_method(id1, id2, go_dag, term_counts, highest_ic_anc))


# def _do_compute_summation_set_value(go_list1, go_list2, term_counts, go_dag, highest_ic_anc, similarity_method=rel_metric):
#     # go_list2 must stay the same between all processes
#     summation_set = 0.0
#     for id1 in go_list1:
#         similarity_values = []
#         for id2 in go_list2:
#             similarity_values.append(similarity_method(id1, id2, go_dag, term_counts, highest_ic_anc))
#         summation_set += max(similarity_values + [NAN_VALUE])
#     return summation_set
#
#
# def parallel_compute_bma_metric(go_list1, go_list2, term_counts, go_dag, highest_ic_anc, similarity_method=rel_metric):
#




def compute_bma_metric(go_list1, go_list2, term_counts, go_dag, highest_ic_anc, similarity_method=rel_metric):
    """calculate the best match average similarity of the two provided sets of go terms

    For each GO term in go_list1, the similarity value of the most similar term from go_list2 is picked. The sum of
    these highest similarity values is divided by the total number of GO terms in go_list1 and go_list2. The metric
    is implemented according to: Schlicker, A., Domingues, F.S., Rahnenführer, J. et al. A new measure for functional
    similarity of gene products based on Gene Ontology. BMC Bioinformatics 7, 302 (2006) doi:10.1186/1471-2105-7-302

    Parameters
    ----------
    go_list1 : iterable
        iterable, containing go term strings
    go_list2 : iterable
        iterable, containing go term strings
    term_counts : dict
        dictionary: key: GO terms, values: number of occurrences of GO term and its children in body of evidence
    go_dag : GODag object
        GODag object from the goatools package
    highest_ic_anc : dict
        dictionary: key: GO terms, values: information content of the ancestor with the highest information content
    similarity_method : function
        function with the following arguments: id1, id2, go_dag, term_counts, highest_ic_anc
        must return a float or the value of the global variable NAN_VALUE.


    Returns
    -------
    float

    """

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
    if (len(go_list1) + len(go_list2)) == 0:
        bma = 0
    else:
        bma = (summation_set12 + summation_set21) / (len(go_list1) + len(go_list2))
    return bma
