from .tt_explorer import TTExplorer
from IPython.display import IFrame


def embed_in_notebook(explorer: TTExplorer, model_path: str, node_data=[]):
    url = explorer.get_rendered_url(model_path=model_path, node_data=node_data)
    return IFrame(url, 900, 500)
