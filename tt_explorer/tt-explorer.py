from flask import Flask, render_template, request, abort, jsonify
from werkzeug.datastructures import FileStorage
from urllib.parse import quote
import model_explorer
import threading
import requests
import json

# Define all the model explorer API functionality and instantiate an instance in a thread.

model_explorer_config = model_explorer.config()
model_explorer_url = 'http://localhost'
model_explorer_port = 5006
POST_ENDPOINT = f'{model_explorer_url}:{model_explorer_port}/apipost/v1/'
GET_ENDPOINT = f'{model_explorer_url}:{model_explorer_port}/api/v1/'

def upload_from_file(file_path) -> str:
    with open(file_path, 'r') as f:
        resp = requests.post(POST_ENDPOINT + '/upload', files={'file': f})
        assert resp.ok
        return resp.json()['path'] # Return temporary path provided by model-explorer

def process_model(model_path) -> dict:
    # Returns graph of processed .ttir model
    cmd = {
        'extensionId': 'tt_adapter',
        'cmdId': 'convert',
        'modelPath': model_path,
        'deleteAfterConversion': False,
        'settings': {}
    }
    resp = requests.post(POST_ENDPOINT + '/send_command', json=cmd)
    return resp.json()

def rendered_graph_url(model_path) -> str:
    # Returns URL for model-explorer that renders that model_path
    url_data = {'models': [{'url': model_path}]}
    return f'{model_explorer_url}:{model_explorer_port}/?show_open_in_new_tab=1&data={quote(json.dumps(url_data))}'

def run_model_explorer():
    global model_explorer_url
    # model_explorer_url += f':{model_explorer_port}/?show_open_in_new_tab=1&data={model_explorer_config.to_url_param_value()}'
    model_explorer.visualize_from_config(
        config=model_explorer_config,
        no_open_in_browser=True,
        port=model_explorer_port,
        extensions=['tt_adapter'] # Reliant on PR #85 [https://github.com/google-ai-edge/model-explorer/pull/85] 
    )

# Define all the API functionality for the user to begin rendering their own Model Explorer instances

app = Flask(__name__)

# TODO: Create GUI powered by API
@app.route('/')
def index(): 
   return render_template('index.html')


# TODO: Plan out API skeleton to function with only model_path

@app.route('/api/add_model', methods=['POST'])
def add_model():
    if 'file' not in request.files:
        abort(400, "No file provided")
    file = request.files['file']
    storage = FileStorage(file.stream, filename=file.filename, name=file.filename)
    resp = requests.post(POST_ENDPOINT + '/upload', files={'file': storage})
    assert resp.ok
    return jsonify(resp.json())

@app.route('/api/render_url', methods=['GET'])
def render_url():
    if 'model_path' not in request.args:
        abort(400, "Provide a model_path in Request Parameters")
    return jsonify({'url': rendered_graph_url(request.args.get('model_path'))})

@app.route('/api/get_graph', methods=['GET'])
def get_graph():
    if 'model_path' not in request.args:
        abort(400, "Provide a model_path in Request Parameters")
    model_path = request.args.get('model_path')
    print(process_model(model_path))
    return jsonify(process_model(model_path))

@app.route('/api/get_nodes', methods=['GET'])
def get_nodes():
    if not request.is_json():
        abort(415, "Please provide a JSONified Graph")
    graph = request.json['graphs'][0] # Index the first graph!
    # Need to parse through nodes and only get elements in [id, label, namespace, attrs]
    # Do it the pythonic way
    nodes = [
        {key: graph['nodes'][i][key] for key in graph['nodes'][i] if key in ['id', 'label', 'namespace', 'attrs']}
            for i in range(len(graph['nodes']))]

    return jsonify({'nodes': nodes})

@app.route('/api/get_attributes', methods=['GET'])
def get_attributes():
    if not request.is_json():
        abort(415, "Please provide a JSON Request")
    if 'node_id' not in request.args:
        abort(400, "Include node_id in the request arguments")
    node_id = request.args.get('node_id')
    graph = request.json['graphs'][0]

    return jsonify({'attrs': [node['attrs'] for node in graph['nodes'] if node['id'] == node_id]})


@app.route('/api/set_attribute', methods=['POST'])
def set_attributes():
    if not request.is_json():
        abort(415, "Please provide a JSONified graph")
    if any(x not in request.args for x in ['node_id', 'attr_key', 'attr_value']):
        abort(400, "Please provide node_id, attr_key, attr_value in request arguemnts")
    node_id = request.args.get('node_id')
    attr_key = request.args.get('attr_key')
    attr_value = request.args.get('attr_value')
    graph = request.json['graphs'][0]

    # Another pythonic call to get the Node Index by the id
    node_idx = [i for i, node in enumerate(graph['nodes']) if node['id'] == node_id][0]
    attrs = graph['nodes'][node_idx]['attrs']
    for attr in attrs:
        if attr['key'] == attr_key:
            attr['value'] = attr_value

    return 200

# TODO: Create Python-Headed API for Jupyter Notebooks and such



if __name__ == '__main__':
    # Begin the Model Explorer with tt_adapter extension
    model_explorer_thread = threading.Thread(target = run_model_explorer)
    model_explorer_thread.start()

    
    app.run(port=5007)