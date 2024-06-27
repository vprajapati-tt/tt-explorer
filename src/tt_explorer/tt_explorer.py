from urllib.parse import quote
import model_explorer
import threading
import requests
import json


class TTExplorer:
    def __init__(self, port=5006, url="http://localhost", config=None):
        # "Public" Objects
        self.model_explorer_port = port
        self.model_explorer_url = f"{url}:{port}/"
        self.POST_ENDPOINT = self.model_explorer_url + "apipost/v1/"
        self.GET_ENDPOINT = self.model_explorer_url + "api/v1/"
        # "Hidden" Objects
        self._model_explorer_config = config if config else model_explorer.config()
        self._model_explorer_thread = threading.Thread(
            target=lambda: model_explorer.visualize_from_config(
                config=self._model_explorer_config,
                no_open_in_browser=True,
                port=self.model_explorer_port,
                extensions=["tt_adapter"],
            )
        )
        # Start the model_explorer server to start using it.
        self._model_explorer_thread.start()

    def get_model_path(self, file) -> str:
        resp = requests.post(self.POST_ENDPOINT + "upload", files={"file": f})
        assert resp.ok
        return resp.json()["path"]  # Temporary Path provided by File

    def get_graph(self, model_path: str, settings={}):
        cmd = {
            "extensionId": "tt_adapter",
            "cmdId": "convert",
            "model_path": model_path,
            "deleteAfterConversion": False,
            "settings": settings,
        }
        resp = requests.post(self.POST_ENDPOINT + "send_command", json=cmd)
        assert resp.ok
        return resp.json()

    def get_rendered_url(self, model_path: str, node_data=[]):
        url_data = {"models": [{"url": model_path}], "nodeData": node_data}
        return f"{self.model_explorer_url}?show_open_in_new_tab=1&data={quote(json.dumps(url_data))}"

    def load_new_graph(self, filepath: str):
        # This will load a new graph through the pure JSON adapter in model_explorer
        pass


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="", type=int)
    parser.add_argument("-u", "--url", help="")

    args = parser.parse_args()

    if args.port and args.url:
        explorer = TTExplorer(args.port, args.url)
    elif args.port:
        explorer = TTExplorer(args.port)
    else:
        explorer = TTExplorer()

    return explorer


if __name__ == "__main__":
    main()
