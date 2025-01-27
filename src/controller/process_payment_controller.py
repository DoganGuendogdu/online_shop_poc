from src.model.payment_methods_model import *
from src.view.process_payment_view import ProcessPaymentView


class ProcessPaymentController:
    def __init__(self, process_payment_view: ProcessPaymentView):
        self.__process_payment_view = process_payment_view
        self.__payment_model = PaymentStrategy()

    def process_payment(self):
        payment_credential_details = self.__process_payment_view.get_payment_method_credentials()

        if payment_credential_details:
            payment_type = payment_credential_details.get("payment_type")

            if payment_type == "PayPal":
                self.__payment_model.set_payment_method(self.__process_paypal_payment(payment_credential_details))
                self.__payment_model.set_seller_protection_for_buyer(PaypalBuyerProtectionStrategy())

            elif payment_type == "Credit card":
                self.__payment_model.set_payment_method(self.__process_credit_card_payment(payment_credential_details))
                self.__payment_model.set_seller_protection_for_buyer(CreditCardBuyerProtectionStrategy())

            elif payment_type == "PaySafe":
                self.__payment_model.set_payment_method(self.__process_paysafe_payment(payment_credential_details))
                self.__payment_model.set_seller_protection_for_buyer(PaysafeBuyerProtectionStrategy())

            elif payment_type == "Apple Pay":
                self.__payment_model.set_payment_method(self.__process_apple_pay_payment(payment_credential_details))
                self.__payment_model.set_seller_protection_for_buyer(ApplePayBuyerProtectionStrategy())
            else:
                raise Exception("No valid payment type provided")

            self.__payment_model.print_payment_params()
            self.__payment_model.print_seller_protection_for_buyer()

    def __process_paypal_payment(self, payment_credential_details):
        paypal_user_name = payment_credential_details.get("paypal_user_name")
        paypal_password = payment_credential_details.get("paypal_password")
        paypal_payment = PayPalStrategy(paypal_user_name, paypal_password)
        return paypal_payment

    def __process_credit_card_payment(self, payment_credential_details):
        credit_card_number = payment_credential_details.get("credit_card_number")
        expiration_date = payment_credential_details.get("expiration_date")
        cvc_number = payment_credential_details.get("cvc_number")
        first_name = payment_credential_details.get("first_name")
        last_name = payment_credential_details.get("last_name")
        credit_card_payment = CreditCardStrategy(credit_card_number, expiration_date, cvc_number, first_name, last_name)
        return credit_card_payment

    def __process_paysafe_payment(self, payment_credential_details):
        paysafe_code = payment_credential_details.get("paysafe_code")
        paysafe_payment = PaysafeStrategy(paysafe_code)
        return paysafe_payment

    def __process_apple_pay_payment(self, payment_credential_details):
        apple_id = payment_credential_details.get("apple_id")
        apple_id_password = payment_credential_details.get("apple_id_password")
        apple_pay_payment = ApplePayStrategy(apple_id, apple_id_password)
        return apple_pay_payment
