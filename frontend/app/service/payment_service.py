import logging

import requests as re


class PaymentService:
    def __init__(self):
        self.__logger = logging.getLogger("payment_logger")

    def post_payment_request(self, payment_input: dict):
        payment_type = payment_input.get("payment_type")

        if not payment_type:
            self.__logger.debug("Can not handle payment process using API. 'payment_type' is None in {payment_input}.")
            raise ValueError(f"Can not handle payment process using API. 'payment_type' is None in {payment_input}.")

        if payment_type == "paypal":
            paypal_user_name = payment_input.get("paypal_user_name")
            paypal_password = payment_input.get("paypal_password")
            return self.__post_paypal_payment_request(paypal_user_name, paypal_password)

    def __post_paypal_payment_request(self, paypal_user_name: str, paypal_password: str):
        paypal_url = "http://127.0.0.1:1111/payment/paypal"

        paypal_input_data = {
            "email": paypal_user_name,
            "password": paypal_password
        }

        self.__logger.debug("Sending POST request for 'paypal' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{paypal_url}'")
        self.__logger.debug(f"Created JSON input data: '{paypal_input_data}'")

        try:
            self.__logger.debug("Sending POST request to endpoint")
            paypal_request = re.post(paypal_url, json=paypal_input_data)
            self.__logger.debug(f"Response '{paypal_request}'.")
            return paypal_request
        except re.HTTPError as e:
            logging.debug(f"Error while sending POST request to endpoint '{paypal_url}': {e}.")
