# main.py

from typing import Dict
from model_explorer import Adapter, AdapterMetadata, ModelExplorerGraphs, graph_builder
from collections import defaultdict
from ttmlir.ir import ir
from ttmlir.dialects import ttkernel, tt, ttir

class TTAdapter(Adapter):

  metadata = AdapterMetadata(id='tt_adapter',
                             name='Tenstorrent Adapter',
                             description='Prototype adapter from TT BUDA to Model Explorer',
                             source_repo='https://github.com/vprajapati-tt/tt-explorer',
                             fileExts=['ttir'])

  # Required.
  def __init__(self):
    super().__init__()

  def convert(self, model_path: str, settings: Dict) -> ModelExplorerGraphs:
    f = open(model_path, 'r')
    name_dict = defaultdict(int)
    connections = defaultdict(int)
    value_dict = {}

    graph = graph_builder.Graph(id='ttir-graph')


    with ir.Context() as ctx:
        ttkernel.register_dialect(ctx)
        module = ir.Module.parse(''.join(f.readlines()), ctx)
        for op in module.body.operations:
            # High level functions, need to list their arguments in the graph
            name_num = name_dict[op.name]
            id = op.name + str(name_num)
            graph.nodes.append(graph_builder.GraphNode(id=id, label=op.name))
            for arg in op.arguments:
                value_dict[arg.get_name()] = graph.nodes[-1]
            
            for region in op.regions:
                for block in region.blocks:
                    for op in block.operations:
                        # Just list out the nodes and assign their ids
                        name_num = name_dict[op.name]
                        id = op.name + str(name_num)
                        graph.nodes.append(graph_builder.GraphNode(id=id, label=op.name))
                        for result in op.results:
                            # Attach the graph node here
                            value_dict[result.get_name()] = graph.nodes[-1]
                        
                        for ops in op.operands:
                            # Guaranteed topological ordering, so we can start to connect previous values to their respective operations
                            source_node = value_dict[ops.get_name()]
                            graph.nodes[-1].incomingEdges.append(graph_builder.IncomingEdge(
                               sourceNodeId=source_node.id,
                               sourceNodeOutputId=str(connections[source_node.id]),
                            ))

                            graph.nodes[-1].outputsMetadata()

    return {'graphs': []}