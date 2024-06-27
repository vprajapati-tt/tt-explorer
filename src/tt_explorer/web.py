from flask import Flask, render_template, request, abort, jsonify
from werkzeug.datastructures import FileStorage
from .tt_explorer import TTExplorer
import threading
import requests


app = Flask(__name__)

# TODO: Create GUI powered by API
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/add_model", methods=["POST"])
def add_model():
    if "file" not in request.files:
        abort(400, "No file provided")
    file = request.files["file"]
    storage = FileStorage(file.stream, filename=file.filename, name=file.filename)
    resp = requests.post(POST_ENDPOINT + "/upload", files={"file": storage})
    assert resp.ok
    return jsonify(resp.json())


@app.route("/api/render_url", methods=["GET"])
def render_url():
    if "model_path" not in request.args:
        abort(400, "Provide a model_path in Request Parameters")
    return jsonify({"url": rendered_graph_url(request.args.get("model_path"))})


@app.route("/api/get_graph", methods=["GET"])
def get_graph():
    if "model_path" not in request.args:
        abort(400, "Provide a model_path in Request Parameters")
    model_path = request.args.get("model_path")
    print(process_model(model_path))
    return jsonify(process_model(model_path))


@app.route("/api/get_nodes", methods=["GET"])
def get_nodes():
    if not request.is_json():
        abort(415, "Please provide a JSONified Graph")
    graph = request.json["graphs"][0]  # Index the first graph!
    # Need to parse through nodes and only get elements in [id, label, namespace, attrs]
    # Do it the pythonic way
    nodes = [
        {
            key: graph["nodes"][i][key]
            for key in graph["nodes"][i]
            if key in ["id", "label", "namespace", "attrs"]
        }
        for i in range(len(graph["nodes"]))
    ]

    return jsonify({"nodes": nodes})


@app.route("/api/get_attributes", methods=["GET"])
def get_attributes():
    if not request.is_json():
        abort(415, "Please provide a JSON Request")
    if "node_id" not in request.args:
        abort(400, "Include node_id in the request arguments")
    node_id = request.args.get("node_id")
    graph = request.json["graphs"][0]

    return jsonify(
        {"attrs": [node["attrs"] for node in graph["nodes"] if node["id"] == node_id]}
    )


@app.route("/api/set_attribute", methods=["POST"])
def set_attributes():
    if not request.is_json():
        abort(415, "Please provide a JSONified graph")
    if any(x not in request.args for x in ["node_id", "attr_key", "attr_value"]):
        abort(400, "Please provide node_id, attr_key, attr_value in request arguemnts")
    node_id = request.args.get("node_id")
    attr_key = request.args.get("attr_key")
    attr_value = request.args.get("attr_value")
    graph = request.json["graphs"][0]

    # Another pythonic call to get the Node Index by the id
    node_idx = [i for i, node in enumerate(graph["nodes"]) if node["id"] == node_id][0]
    attrs = graph["nodes"][node_idx]["attrs"]
    for attr in attrs:
        if attr["key"] == attr_key:
            attr["value"] = attr_value

    return 200


# TODO: Create Python-Headed API for Jupyter Notebooks and such


if __name__ == "__main__":
    # Begin the Model Explorer with tt_adapter extension
    model_explorer_thread = threading.Thread(target=run_model_explorer)
    model_explorer_thread.start()

    app.run(port=5007)
