import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parent.parent


class Config:
    def __init__(self):
        self.__config_path = Path(PROJECT_ROOT) / "config.json"

    def get_payment_methods(self):
        with open(self.__config_path, "r") as json_file:
            config = json.load(json_file)
            return config["payment_methods"]
