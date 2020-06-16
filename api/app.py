from flask import Flask, request, Response
from megago.megago import run_comparison, get_default_go_dag, find_non_existing_terms

app = Flask(__name__)

# Load the GO_DAG only once for the complete application to speed up computation of comparisons
GO_DAG = get_default_go_dag()


@app.route('/')
def index():
    return 'index'


@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.get_json(silent=True)

    # Check whether the given data is actually valid
    if not data or "sample1" not in data or "sample2" not in data:
        return Response(status=422)

    go_list1 = data["sample1"]
    go_list2 = data["sample2"]

    not_present = find_non_existing_terms(go_list1, GO_DAG)
    not_present.update(find_non_existing_terms(go_list2, GO_DAG))

    result = run_comparison(go_list1, go_list2, GO_DAG)

    return {
        "similarity": {
            "biological_process": result[0],
            "cellular_component": result[1],
            "molecular_function": result[2]
        },
        "invalid": list(not_present)
    }
