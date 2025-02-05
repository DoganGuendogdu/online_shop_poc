from ..models.payment_methods_model import *


class ProcessPaymentController:
    def __init__(self):
        self.__payment_model = PaymentModel()

    def get_PayPal_payment_details(self, paypal_user_name: str, paypal_password: SecretStr):
        paypal_model = PayPalModel(email=paypal_user_name, password=paypal_password)
        self.__payment_model.set_payment_method(PayPalStrategy(paypal_model))
        return self.__payment_model.get_payment_details()

    def get_master_card_payment_details(self, credit_card_number: str, expiration_date: datetime, cvc_number: int,
                                        first_name: str, last_name: str):
        credit_card_model = MasterCardModel(credit_card_number=credit_card_number, expiration_date=expiration_date,
                                            cvc=cvc_number, first_name=first_name, last_name=last_name)
        self.__payment_model.set_payment_method(MasterCardStrategy(credit_card_model))
        return self.__payment_model.get_payment_details()

    def get_PaySafe_payment_details(self, paysafe_code: str):
        paysafe_model = PaySafeModel(paysafe_code=paysafe_code)
        self.__payment_model.set_payment_method(PaySafeStrategy(paysafe_model))
        return self.__payment_model.get_payment_details()

    def get_ApplePay_payment_details(self, apple_id: str, apple_id_password: str):
        apple_pay_model = ApplePayModel(apple_id=apple_id, password=apple_id_password)
        self.__payment_model.set_payment_method(ApplePayStrategy(apple_pay_model))
        return self.__payment_model.get_payment_details()
