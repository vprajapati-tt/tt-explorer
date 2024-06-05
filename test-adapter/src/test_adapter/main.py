# main.py

from typing import Dict
from model_explorer import Adapter, AdapterMetadata, ModelExplorerGraphs, graph_builder
import json
from collections import defaultdict

class TestAdapter(Adapter):

  metadata = AdapterMetadata(id='my_adapter',
                             name='My first adapter',
                             description='My first adapter!',
                             source_repo='https://github.com/user/my_adapter',
                             fileExts=['test'])

  # Required.
  def __init__(self):
    super().__init__()

  def convert(self, model_path: str, settings: Dict) -> ModelExplorerGraphs:
    read_graph = json.load(open(model_path, 'r'))

    graph = graph_builder.Graph(id='testing-graph')
    connections = defaultdict(int)

    for node in read_graph['nodes']:
        node = defaultdict(str, **node)
        graph.nodes.append(graph_builder.GraphNode(id=node['id'], label=node['operation'], namespace=node['namespace']))
    
    for node in read_graph['nodes']:
        node = defaultdict(str, **node)
        this_node = graph.nodes[int(node['id'][4:]) - 1]
        for input_node in node['inputs']:
            this_node.incomingEdges.append(graph_builder.IncomingEdge(
                sourceNodeId=input_node, sourceNodeOutputId=str(connections[input_node])))
            this_node.inputsMetadata.append(graph_builder.MetadataItem(
               id=str(connections[input_node]), attrs=[graph_builder.KeyValue(key='__tensor_tag', value=input_node),
                                                       graph_builder.KeyValue(key='TensorSize', value=str(node['tensorSize']))]
            ))
            connections[input_node] += 1

    return {'graphs': [graph]}