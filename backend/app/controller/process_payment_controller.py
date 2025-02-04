from datetime import datetime

from ..models.payment_methods_model import *


class ProcessPaymentController:
    def __init__(self):
        self.__payment_model = PaymentModel()

    def get_PayPal_payment_details(self, paypal_user_name: str, paypal_password: str):
        self.__payment_model.set_payment_method(PayPalStrategy(paypal_user_name, paypal_password))
        return self.__payment_model.get_payment_details()

    def get_credict_card_payment_details(self, credit_card_number: int, expiration_date: datetime, cvc_number: int,
                                         first_name: str, last_name: str):
        self.__payment_model.set_payment_method(
            CreditCardStrategy(credit_card_number, expiration_date, cvc_number, first_name, last_name))
        return self.__payment_model.get_payment_details()

    def get_PaySafe_payment_details(self, paysafe_code: int):
        self.__payment_model.set_payment_method(PaysafeStrategy(paysafe_code))
        return self.__payment_model.get_payment_details()

    def get_ApplePay_payment_details(self, apple_id: str, apple_id_password: str):
        self.__payment_model.set_payment_method(ApplePayStrategy(apple_id, apple_id_password))
        return self.__payment_model.get_payment_details()

        # self.__payment_model.print_seller_protection_for_buyer()

    # def process_payment(self, payment_method):
    #
    #     if payment_method:
    #         payment_type = payment_method.get("payment_type")
    #
    #         if payment_type == "PayPal":
    #             self.__payment_model.set_payment_method(self.get_paypal_payment_details(payment_method))
    #             self.__payment_model.set_seller_protection_for_buyer(PaypalBuyerProtectionStrategy())
    #
    #         elif payment_type == "Credit card":
    #             self.__payment_model.set_payment_method(self.get_credit_card_payment_details(payment_method))
    #             self.__payment_model.set_seller_protection_for_buyer(CreditCardBuyerProtectionStrategy())
    #
    #         elif payment_type == "PaySafe":
    #             self.__payment_model.set_payment_method(self.get_paysafe_payment_details(payment_method))
    #             self.__payment_model.set_seller_protection_for_buyer(PaysafeBuyerProtectionStrategy())
    #
    #         elif payment_type == "Apple Pay":
    #             self.__payment_model.set_payment_method(self.get_apple_pay_payment_details(payment_method))
    #             self.__payment_model.set_seller_protection_for_buyer(ApplePayBuyerProtectionStrategy())
    #         else:
    #             raise Exception("No valid payment type provided")
    #
    #         self.__payment_model.print_payment_params()
    #         self.__payment_model.print_seller_protection_for_buyer()

    # def get_paypal_payment_details(self, payment_credential_details):
    #     paypal_user_name = payment_credential_details.get("paypal_user_name")
    #     paypal_password = payment_credential_details.get("paypal_password")
    #     paypal_payment = PayPalStrategy(paypal_user_name, paypal_password)
    #     return paypal_payment
    #
    # def get_credit_card_payment_details(self, payment_credential_details):
    #     credit_card_number = payment_credential_details.get("credit_card_number")
    #     expiration_date = payment_credential_details.get("expiration_date")
    #     cvc_number = payment_credential_details.get("cvc_number")
    #     first_name = payment_credential_details.get("first_name")
    #     last_name = payment_credential_details.get("last_name")
    #     credit_card_payment = CreditCardStrategy(credit_card_number, expiration_date, cvc_number, first_name, last_name)
    #     return credit_card_payment
    #
    # def get_paysafe_payment_details(self, payment_credential_details):
    #     paysafe_code = payment_credential_details.get("paysafe_code")
    #     paysafe_payment = PaysafeStrategy(paysafe_code)
    #     return paysafe_payment

    # def get_apple_pay_payment_details(self, payment_credential_details):
    #     apple_id = payment_credential_details.get("apple_id")
    #     apple_id_password = payment_credential_details.get("apple_id_password")
    #     apple_pay_payment = ApplePayStrategy(apple_id, apple_id_password)
    #     return apple_pay_payment
