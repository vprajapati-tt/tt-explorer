from urllib.parse import quote
import model_explorer
import threading
import requests
import json


class TTExplorer:
    def __init__(self, port=8080, url="http://localhost", server=False, config=None):
        # "Public" Objects
        self.model_explorer_port = port
        self.model_explorer_url = f"{url}:{port}/"
        self.POST_ENDPOINT = self.model_explorer_url + "apipost/v1/"
        self.GET_ENDPOINT = self.model_explorer_url + "api/v1/"

        # If creating server:
        self.IS_SERVER = server
        if self.IS_SERVER:
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
            self._model_explorer_thread.daemon = True
            self._model_explorer_thread.start()

    def get_model_path(self, file) -> str:
        resp = requests.post(self.POST_ENDPOINT + "upload", files={"file": file})
        assert resp.ok
        return resp.json()["path"]  # Temporary Path provided by File

    def execute_model(self, model_path: str, settings={}):
        cmd = {
            "extensionId": "tt_adapter",
            "cmdId": "execute",
            "model_path": model_path,
            "deleteAfterConversion": False,
            "settings": settings,
        }
        resp = requests.post(self.POST_ENDPOINT + "send_command", json=cmd)
        assert resp.ok
        return resp.json()

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


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="", type=int)
    parser.add_argument("-u", "--url", help="")

    args = parser.parse_args()

    if args.port and args.url:
        explorer = TTExplorer(args.port, args.url, server=True)
    elif args.port:
        explorer = TTExplorer(args.port, server=True)
    else:
        explorer = TTExplorer(server=True)

    return explorer


if __name__ == "__main__":
    main()
