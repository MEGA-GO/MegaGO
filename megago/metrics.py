import math
import concurrent.futures
import os

from goatools.obo_parser import GODag
from goatools.semantic import deepest_common_ancestor
from goatools.gosubdag.gosubdag import GoSubDag

from .constants import NAN_VALUE, GO_DAG_FILE_PATH

PROCESSES = 6
CHUNK_SIZE = 50


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
    return deepest_common_ancestor([id1, id2], go_dag)


def rel_metric(c1, c2, go_dag, term_counts, highest_ic_anc):
    """calculate semantic similarity of the GO terms id1 and id2 using the rel metric

    Formula of the metric: (2 * info_content(mica) * (1 - freq(mica))) / (info_content(go_id1) + info_content(go_id2))
    where mica is the most informative common ancestor of go_id1 and go_id2.
    Metric is implemented according to: Schlicker, A., Domingues, F.S., Rahnenführer, J. et al. A new measure for
    functional similarity of gene products based on Gene Ontology. BMC Bioinformatics 7, 302 (2006)
    doi:10.1186/1471-2105-7-302


    Parameters
    ----------
    c1 : str
        GO term
    c2 : str
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

    if (c1 not in go_dag) or (c2 not in go_dag):
        return NAN_VALUE

    go_term1 = go_dag[c1]
    go_term2 = go_dag[c2]
    if go_term1.namespace == go_term2.namespace:
        lca_goid = get_deepest_common_ancestor(c1, c2, go_dag)
        freq = get_frequency(lca_goid, term_counts, go_dag)
        info_content_lca = get_info_content(lca_goid, term_counts, go_dag)
        info_content1 = get_info_content(c1, term_counts, go_dag)
        info_content2 = get_info_content(c2, term_counts, go_dag)
        if info_content1 == 0:
            info_content1 = highest_ic_anc[c1]
        if info_content2 == 0:
            info_content2 = highest_ic_anc[c2]
        if info_content1 + info_content2 == 0:
            return 0
        return (2 * info_content_lca * (1 - freq)) / (info_content1 + info_content2)
    else:    # if goterms are from different GO namespaces (molecular function, cellular component, biological process)
        return NAN_VALUE


def lin_metric(c1, c2, go_dag, term_counts, highest_ic_anc):
    """calculate semantic similarity of the GO terms id1 and id2 using the rel metric

    Formula of the metric: (2 * info_content(mica)) / (info_content(go_id1) + info_content(go_id2))
    where mica is the most informative common ancestor of go_id1 and go_id2.

    Metric is implemented according to: Lin, Dekang. 1998. “An Information-Theoretic Definition of Similarity.” In
    Proceedings of the 15th International Conference on Machine Learning, 296—304.


    Parameters
    ----------
    c1 : str
        GO term
    c2 : str
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
    if (c1 not in go_dag) or (c2 not in go_dag):
        return NAN_VALUE

    go_term1 = go_dag[c1]
    go_term2 = go_dag[c2]
    if go_term1.namespace == go_term2.namespace:
        lca_goid = get_deepest_common_ancestor(c1, c2, go_dag)
        info_content_lca = get_info_content(lca_goid, term_counts, go_dag)
        info_content1 = get_info_content(c1, term_counts, go_dag)
        info_content2 = get_info_content(c2, term_counts, go_dag)
        if info_content1 == 0:
            info_content1 = highest_ic_anc[c1]
        if info_content2 == 0:
            info_content2 = highest_ic_anc[c2]
        if info_content1 + info_content2 == 0:
            return 0
        return (2 * info_content_lca) / (info_content1 + info_content2)
    else:    # if goterms are from different GO namespaces (molecular function, cellular component, biological process)
        return NAN_VALUE


def compute_similarity_method(params):
    (go_list1, go_list2, term_counts, go_dag_path, highest_ic_anc, similarity_method) = params
    go_dag = GODag(GO_DAG_FILE_PATH, prt=open(os.devnull, 'w'))
    result = dict()

    for id1 in go_list1:
        for id2 in go_list2:
            key = (id1, id2) if id1 < id2 else (id2, id1)
            result[key] = similarity_method(id1, id2, go_dag, term_counts, highest_ic_anc)
    return result


def compute_bma_metric(go_list1, go_list2, term_counts, highest_ic_anc, progress_listener=None, similarity_method="rel"):
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
    highest_ic_anc : dict
        dictionary: key: GO terms, values: information content of the ancestor with the highest information content
    progress_listener: function (number) => void
        is called with comparisons that currently have been performed
    similarity_method : string
        choose between lin and rel metric. 'lin' -> lin_metric, 'rel' -> rel_metric

    Returns
    -------
    float

    """

    unique_list1 = list(set(go_list1))
    unique_list2 = list(set(go_list2))

    # Store the results of the similarity method in this dictionary
    sim_method_dict = dict()

    amount_of_chunks = math.ceil(len(unique_list1) / CHUNK_SIZE)

    sim_func = None
    if similarity_method == "lin":
        sim_func = lin_metric
    elif similarity_method == "rel":
        sim_func = rel_metric
    else:
        raise AttributeError(f"similarity_method must be in ['lin', 'rel'] but is {similarity_method}")

    with concurrent.futures.ProcessPoolExecutor(max_workers=PROCESSES) as executor:
        chunks = []
        for process in range(amount_of_chunks):
            if process == amount_of_chunks - 1:
                chunks.append((unique_list1[CHUNK_SIZE * process:], unique_list2, term_counts, GO_DAG_FILE_PATH, highest_ic_anc, sim_func))
            else:
                chunks.append((unique_list1[CHUNK_SIZE * process: CHUNK_SIZE * (process + 1)], unique_list2, term_counts, GO_DAG_FILE_PATH, highest_ic_anc, sim_func))
        for result in executor.map(compute_similarity_method, chunks):
            progress_listener(len(result))
            sim_method_dict.update(result)


    summation_set12 = 0.0
    summation_set21 = 0.0

    for id1 in go_list1:
        max_value = 0.0
        for id2 in go_list2:
            key = (id1, id2) if id1 < id2 else (id2, id1)
            value = sim_method_dict[key]
            if value > max_value:
                max_value = value
        if len(go_list2) == 0:
            max_value = NAN_VALUE
        summation_set12 += max_value
    for id2 in go_list2:
        max_value = 0.0
        for id1 in go_list1:
            key = (id1, id2) if id1 < id2 else (id2, id1)
            value = sim_method_dict[key]
            if value > max_value:
                max_value = value
        if len(go_list1) == 0:
            max_value = NAN_VALUE
        summation_set21 += max_value

    if (len(go_list1) + len(go_list2)) == 0:
        bma = 0
    else:
        bma = (summation_set12 + summation_set21) / (len(go_list1) + len(go_list2))
    return bma
