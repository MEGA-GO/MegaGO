from flask import Flask, request, Response
from megago.megago import run_comparison, get_default_go_dag, find_non_existing_terms
from flask_cors import CORS, cross_origin
from threading import Thread

import uuid


app = Flask(__name__)

# Load the GO_DAG only once for the complete application to speed up computation of comparisons
GO_DAG = get_default_go_dag()
# Maps analysis ID to current progress and results once they are available.
RESULTS = dict()


@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze():
    data = request.get_json(silent=True)

    # Check whether the given data is actually valid
    if not data or "sample1" not in data or "sample2" not in data:
        return Response(status=422)

    go_list1 = data["sample1"]
    go_list2 = data["sample2"]

    id = str(uuid.uuid4())

    thread = Compute(go_list1, go_list2, id)
    thread.start()

    return {
        "analysis_id": id
    }


@app.route('/progress/<id>', methods=["POST"])
@cross_origin()
def progress(id):
    if id in RESULTS:
        return {
            "progress": RESULTS[id]["progress"]
        }
    else:
        return Response(status=404)


@app.route('/result/<id>', methods=["POST"])
@cross_origin()
def result(id):
    if id in RESULTS:
        result = RESULTS[id]["result"]
        not_present = RESULTS[id]["not_present"]
        if result:
            return {
                "similarity": {
                    "biological_process": result[0],
                    "cellular_component": result[1],
                    "molecular_function": result[2]
                },
                "invalid": list(not_present)
            }
        else:
            return {
                "error": "Processing of this analysis has not yet finished..."
            }
    else:
        return Response(status=404)


@app.route('/goterms', methods=["POST"])
@cross_origin()
def goterms():
    data = request.get_json(silent=True)

    if not data or "goterms" not in data:
        return Response(status=422)

    processed_terms = []
    for term in data["goterms"]:
        if term in GO_DAG:
            current_term = GO_DAG[term]
            processed_terms.append({
                "code": term,
                "namespace": current_term.namespace,
                "name": current_term.name
            })

    return {
        "goterms": processed_terms
    }


class Compute(Thread):
    def __init__(self, go_list1, go_list2, id):
        Thread.__init__(self)
        self.go_list1 = go_list1
        self.go_list2 = go_list2
        self.id = id

    def run(self):
        metadata = {
            "progress": 0,
            "result": None,
            "not_present": None
        }
        RESULTS[self.id] = metadata

        def update_progress(prog):
            metadata["progress"] = prog

        result = run_comparison(self.go_list1, self.go_list2, GO_DAG, update_progress)

        not_present = find_non_existing_terms(self.go_list1, GO_DAG)
        not_present.update(find_non_existing_terms(self.go_list2, GO_DAG))

        metadata["not_present"] = not_present
        metadata["result"] = result
