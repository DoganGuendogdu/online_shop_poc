import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parent.parent


class Config:
    def __init__(self):
        self.__config_path = Path(PROJECT_ROOT) / "config.json"

        with open(self.__config_path, "r") as json_file:
            config = json.load(json_file)

            self.payment_methods = config["payment_methods"]

            self.paypal_url = config["url"]["paypal"]
            self.paysafe_url = config["url"]["paysafe"]
            self.apple_pay_url = config["url"]["apple_pay"]
            self.master_card_url = config["url"]["master_card"]
