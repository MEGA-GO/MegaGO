import json

from .constants import HEATMAP_TEMPLATE


def read_heatmap_template():
    output = ""
    with open(HEATMAP_TEMPLATE) as f:
        for line in f:
            output += line
    return output


def write_heatmap_template(template):
    with open("heatmap.html", "w") as f:
        f.write(template)


def generate_heatmap(results_dict: dict, sample_names):
    bp_results = []
    cc_results = []
    mf_results = []

    for i, name in enumerate(sample_names):
        bp_row = []
        cc_row = []
        mf_row = []
        for j, name in enumerate(sample_names):
            if i == j:
                bp_row.append(1)
                cc_row.append(1)
                mf_row.append(1)
            elif i < j:
                bp_row.append(results_dict[(i, j)][0])
                cc_row.append(results_dict[(i, j)][1])
                mf_row.append(results_dict[(i, j)][2])
            else:
                bp_row.append(results_dict[(j, i)][0])
                cc_row.append(results_dict[(j, i)][1])
                mf_row.append(results_dict[(j, i)][2])
        bp_results.append(bp_row)
        cc_results.append(cc_row)
        mf_results.append(mf_row)

    heatmap_template = read_heatmap_template()

    heatmap_template = heatmap_template.replace("!!ROW_LABELS!!", json.dumps(sample_names))
    heatmap_template = heatmap_template.replace("!!COL_LABELS!!", json.dumps(sample_names))

    heatmap_template = heatmap_template.replace("!!BP_DATA!!", json.dumps(bp_results))
    heatmap_template = heatmap_template.replace("!!CC_DATA!!", json.dumps(cc_results))
    heatmap_template = heatmap_template.replace("!!MF_DATA!!", json.dumps(mf_results))

    write_heatmap_template(heatmap_template)

