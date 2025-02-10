import logging
from datetime import date
from datetime import datetime
from typing import Union

import requests
from app.config import Config
from requests.models import Response


# TODO: Validate inputs. Check why passwords are exposed. Handle HTTP statuses.
class PaymentService:
    def __init__(self, config: Config):
        self.__paypal_url = config.paypal_url
        self.__master_card_url = config.master_card_url
        self.__paysafe_url = config.paysafe_url
        self.__apple_pay_url = config.apple_pay_url

        self.__logger = logging.getLogger("payment_logger")

    def post_payment(self, payment_input: dict):
        payment_type = payment_input.get("payment_type")

        if not payment_type:
            self.__logger.debug("Can not handle payment process using API. 'payment_type' is None in {payment_input}.")
            raise ValueError(f"Can not handle payment process using API. 'payment_type' is None in {payment_input}.")

        if payment_type == "paypal":
            paypal_user_name = payment_input.get("paypal_username")
            paypal_password = payment_input.get("paypal_password")
            return self.__post_paypal_payment(paypal_user_name, paypal_password)
        elif payment_type == "paysafe":
            paysafe_code = payment_input.get("paysafe_code")
            return self.__post_paysafe_payment(paysafe_code)
        elif payment_type == "apple_pay":
            apple_id = payment_input.get("apple_id")
            apple_password = payment_input.get("apple_id_password")
            return self.__post_apple_pay_payment(apple_id, apple_password)
        elif payment_type == "master_card":
            credit_card_number = payment_input.get("credit_card_number")
            expiration_date = payment_input.get("expiration_date")
            cvc_number = payment_input.get("cvc_number")
            first_name = payment_input.get("first_name")
            last_name = payment_input.get("last_name")
            return self.__post_master_card_payment(credit_card_number, expiration_date, cvc_number, first_name,
                                                   last_name)
        else:
            self.__logger.debug(f"The provided 'payment_type':{payment_type} does not exist.")

    def __post_master_card_payment(self, credit_card_number: int, expiration_date: Union[date, str],
                                   cvc_number: int,
                                   first_name: str, last_name: str):
        self.__logger.info("Processing master card payment.")

        credit_card_number = int(credit_card_number)
        cvc_number = int(cvc_number)

        if len(str(credit_card_number)) != 16:
            self.__logger.debug("Length of 'credit_card_number' is unequal to 16 digits")

        if len(str(cvc_number)) != 3:
            self.__logger.debug("Length of 'cvc' is unequal to 3.")

        if isinstance(expiration_date, str):
            try:
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            except ValueError:
                self.__logger.debug(f"'Expiration date' str: '{expiration_date}' does not meet format '%Y-%m-%d'")

        if isinstance(expiration_date, date):
            try:
                expiration_date = datetime.strftime(expiration_date, "%Y-%m-%d")
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            except ValueError:
                self.__logger.debug(f"'Expiration date' datetime: '{expiration_date}' does not meet format '%Y-%m-%d'")

        current_day_str = datetime.today().strftime("%Y-%m-%d")
        current_day = datetime.strptime(current_day_str, "%Y-%m-%d")

        if expiration_date <= current_day:
            self.__logger.debug(f"The provided 'expiration_date': '{expiration_date}' has expired.")
            return None

        expiration_date = datetime.strftime(expiration_date, "%Y-%m-%d")

        master_card_json = {
            "credit_card_number": credit_card_number,
            "expiration_date": expiration_date,
            "cvc": cvc_number,
            "first_name": first_name,
            "last_name": last_name
        }

        self.__logger.debug("Sending POST request for 'master_card' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__master_card_url}'")
        self.__logger.debug(f"Created JSON data: '{master_card_json}'")

        master_card_request = None
        try:
            self.__logger.debug("Sending POST request to endpoint")
            master_card_request = requests.post(self.__master_card_url, json=master_card_json)
            self.__logger.debug(f"Response '{master_card_request}'.")
            # return master_card_request
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__master_card_url}': {e}.")

        # return self.__is_response_valid(master_card_request)
        return master_card_request

    def __post_apple_pay_payment(self, apple_id: str, apple_password: str):

        apple_pay_json = {
            "apple_id": apple_id,
            "password": apple_password
        }

        self.__logger.debug("Sending POST request for 'apple_pay' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__apple_pay_url}'")
        self.__logger.debug(f"Created JSON data: '{apple_pay_json}'")

        apple_pay_request = None
        try:
            self.__logger.debug("Sending POST request to endpoint")
            apple_pay_request = requests.post(self.__apple_pay_url, json=apple_pay_json)
            self.__logger.debug(f"Response '{apple_pay_request}'.")
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__apple_pay_url}': {e}.")

        return apple_pay_request
        # return self.__is_response_valid(apple_pay_request)

    def __post_paysafe_payment(self, paysafe_code: int):
        if len(str(paysafe_code)) != 16:
            self.__logger.debug(
                "Can not process 'paysafe' payment. The length of the provided code has to be 16 digits long.")
            raise ValueError("Paysafe code is not 16 digits long.")

        paysafe_json = {
            "paysafe_code": paysafe_code
        }

        self.__logger.debug("Sending POST request for 'paysafe' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__paysafe_url}'")
        self.__logger.debug(f"Created JSON data: '{paysafe_json}'")

        paysafe_request = None
        try:
            self.__logger.debug("Sending POST request to endpoint")
            paysafe_request = requests.post(self.__paysafe_url, json=paysafe_json)
            self.__logger.debug(f"Response '{paysafe_request}'.")
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__paysafe_url}': {e}.")

        return paysafe_request
        # return self.__is_response_valid(paysafe_request)

    def __post_paypal_payment(self, paypal_user_name: str, paypal_password: str):
        paypal_request_body = {
            "email": paypal_user_name,
            "password": paypal_password
        }

        self.__logger.debug("Sending POST request for 'paypal' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__paypal_url}'")
        self.__logger.debug(f"Created JSON data: '{paypal_request_body}'")

        paypal_request = None
        try:
            self.__logger.debug("Sending POST request to endpoint")
            paypal_request = requests.post(self.__paypal_url, json=paypal_request_body)
            self.__logger.debug(f"Response '{paypal_request}'.")
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__paypal_url}': {e}.")

        return paypal_request
        # return self.__is_response_valid(paypal_request)

    def __is_response_valid(self, response: Response):
        if response.status_code != 200:
            self.__logger.debug(f"Request failed. Error code: '{response.status_code}'")

        try:
            return response.json()
        except TypeError as e:
            self.__logger.debug(f"Error while returning successful response '{response}' as JSON object: {e}")
