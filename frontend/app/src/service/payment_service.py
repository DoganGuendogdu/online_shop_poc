import logging
from datetime import date
from datetime import datetime

import requests
from email_validator import validate_email, EmailNotValidError
from requests.models import Response

from ..config import Config


# TODO: Validate inputs. Check why passwords are exposed. Handle HTTP statuses. Exclude passwords from logging.
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

    def validate_http_response(self, response: Response):
        try:
            response.json()
        except ValueError as e:
            self.__logger.debug(f"Can not decode response as JSON: {e}.")
            return None

        if response.status_code == 200:
            self.__logger.debug("Response status: '200'")
            # Use 'update' method to allow that 'status' is at first place.
            result = {"status": response.status_code}
            result.update(response.json())
            self.__logger.debug(f"Result: {result}")
            return result

        if response.status_code != 200:
            self.__logger.debug("Request returned with ERROR.")
            error_details = self.__get_error_details(response)
            self.__logger.debug(f"Error details: {error_details}")
            return error_details

    def __post_master_card_payment(self, credit_card_number: int, expiration_date: date, cvc_number: int,
                                   first_name: str, last_name: str):
        self.__logger.info("Processing master card payment.")

        if len(str(credit_card_number)) != 16:
            self.__logger.debug("Length of 'credit_card_number' is unequal to 16 digits")

        if len(str(cvc_number)) != 3:
            self.__logger.debug("Length of 'cvc' is unequal to 3.")

        if isinstance(expiration_date, date):
            try:
                # Convert date object to str to ensure format.
                expiration_date = datetime.strftime(expiration_date, "%Y-%m-%d")
                # Convert date str back to date object.
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            except ValueError:
                self.__logger.debug(f"'Expiration date' datetime: '{expiration_date}' does not meet format '%Y-%m-%d'")

        current_day_str = datetime.today().strftime("%Y-%m-%d")
        current_day = datetime.strptime(current_day_str, "%Y-%m-%d")

        if expiration_date <= current_day:
            self.__logger.debug(f"The provided 'expiration_date': '{expiration_date}' has expired.")
            return None

        expiration_date = datetime.strftime(expiration_date, "%Y-%m-%d")

        master_card_request_body = {
            "credit_card_number": credit_card_number,
            "expiration_date": expiration_date,
            "cvc": cvc_number,
            "first_name": first_name,
            "last_name": last_name
        }

        self.__logger.debug("Sending POST request for 'master_card' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__master_card_url}'")
        self.__logger.debug(f"Created JSON data: '{master_card_request_body}'")

        try:
            self.__logger.debug("Sending POST request to endpoint")
            master_card_response = requests.post(self.__master_card_url, json=master_card_request_body)
            self.__logger.debug(f"Response '{master_card_response}'.")
            return master_card_response
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__master_card_url}': {e}.")
            return None

    def __post_apple_pay_payment(self, apple_id: str, apple_password: str):
        apple_pay_request_body = {
            "apple_id": apple_id,
            "password": apple_password
        }

        self.__logger.debug("Sending POST request for 'apple_pay' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__apple_pay_url}'")
        self.__logger.debug(f"Created JSON data: '{apple_pay_request_body}'")

        try:
            self.__logger.debug("Sending POST request to endpoint")
            apple_pay_response = requests.post(self.__apple_pay_url, json=apple_pay_request_body)
            self.__logger.debug(f"Response '{apple_pay_response}'.")
            return apple_pay_response
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__apple_pay_url}': {e}.")
            return None

    def __post_paysafe_payment(self, paysafe_code: int):
        if len(str(paysafe_code)) != 16:
            self.__logger.debug(
                "Can not process 'paysafe' payment. The length of the provided code has to be 16 digits long.")
            raise ValueError("Paysafe code is not 16 digits long.")

        paysafe_request_body = {
            "paysafe_code": paysafe_code
        }

        self.__logger.debug("Sending POST request for 'paysafe' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__paysafe_url}'")
        self.__logger.debug(f"Created JSON data: '{paysafe_request_body}'")

        try:
            self.__logger.debug("Sending POST request to endpoint")
            paysafe_request = requests.post(self.__paysafe_url, json=paysafe_request_body)
            self.__logger.debug(f"Response '{paysafe_request}'.")
            return paysafe_request
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__paysafe_url}': {e}.")
            return None

    def __post_paypal_payment(self, paypal_user_name: str, paypal_password: str):
        paypal_request_body = {
            "email": paypal_user_name,
            "password": paypal_password
        }

        self.__logger.debug("Sending POST request for 'paypal' payment.")
        self.__logger.debug(f"Defined endpoint for POST request: '{self.__paypal_url}'")

        self.__logger.debug(f"Validating email '{paypal_user_name}'.")
        if not self.__validate_email(paypal_user_name):
            self.__logger.debug("Email is not valid. Returning None.")
            return None
        self.__logger.debug("Email is valid.")

        self.__logger.debug(
            "Validating password."
        )
        if not self.__validate_paypal_password(paypal_password):
            self.__logger.error(
                "Password is not valid."
            )
            return None

        try:
            self.__logger.debug(
                "Sending POST request to endpoint."
            )
            paypal_response = requests.post(self.__paypal_url, json=paypal_request_body)
            self.__logger.debug(f"Response '{paypal_response}'.")
            return paypal_response
        except requests.RequestException as e:
            logging.debug(f"Error while sending POST request to endpoint '{self.__paypal_url}': {e}.")
            return None

    def __get_error_details(self, response: Response):
        response_details = response.json()
        self.__logger.debug(f"Response details '{response_details}'")

        self.__logger.debug("Extracting 'detail' object.")
        detail = response_details.get("detail")

        if not detail:
            self.__logger.debug(f"Can not extract 'detail' from {response_details}. 'detail' does not exist.")
            return None

        try:
            for data in detail:
                error_type = data.get("type")
                error_location = data.get("loc")
                error_message = data.get("msg")
                user_input = data.get("input")

                if not error_type:
                    self.__logger.debug("'error_type' is None.")
                if not error_location:
                    self.__logger.debug("'error_location' is None.")
                if not error_type:
                    self.__logger.debug("'error_type' is None.")
                if not user_input:
                    self.__logger.debug("'user_input' is None.")

                return {
                    "status": response.status_code,
                    "error_type": error_type,
                    "error_location": error_location,
                    "error_message": error_message,
                    "user_input": user_input
                }
        except KeyError as e:
            self.__logger.debug(f"Can not extract details from response. Key does not exist: {e}.")
            return None

    def __validate_email(self, email: str):

        try:
            email_info = validate_email(email)
            return str(email_info.normalized)
        except EmailNotValidError:
            return None

    def __validate_paypal_password(self, paypal_password: str):
        if len(paypal_password) > 88 or len(paypal_password) < 8:
            return None
        return paypal_password
