# main.py

from typing import Dict
from model_explorer import Adapter, AdapterMetadata, ModelExplorerGraphs, graph_builder
import json
from collections import defaultdict

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
    read_graph = json.load(open(model_path, 'r'))
    return {'graphs': []}