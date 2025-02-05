from app.views.process_payment_view import PaymentView
from app.service.payment_service import PaymentService

class PaymentController:
    def __init__(self, payment_view: PaymentView, payment_service:PaymentService):
        self.__payment_view = payment_view
        self.__payment_service = payment_service

    def get_payment_input_data(self):
        self.__payment_view.get_payment_input_data()

# self.__payment_model = PaymentModel()
#
#
# def get_PayPal_payment_details(self, paypal_user_name: str, paypal_password: SecretStr):
#     paypal_model = PayPal(email=paypal_user_name, password=paypal_password)
#     self.__payment_model.set_payment_method(PayPalStrategy(paypal_model))
#     return self.__payment_model.get_payment_details()
#
# def get_master_card_payment_details(self, credit_card_number: int, expiration_date: datetime, cvc_number: int,
#                                     first_name: str, last_name: str):
#     credit_card_model = MasterCard(credit_card_number=credit_card_number, expiration_date=expiration_date,
#                                    cvc=cvc_number, first_name=first_name, last_name=last_name)
#     self.__payment_model.set_payment_method(MasterCardStrategy(credit_card_model))
#     return self.__payment_model.get_payment_details()
#
# def get_PaySafe_payment_details(self, paysafe_code: int):
#     paysafe_model = PaySafe(paysafe_code=paysafe_code)
#     self.__payment_model.set_payment_method(PaySafeStrategy(paysafe_model))
#     return self.__payment_model.get_payment_details()
#
# def get_ApplePay_payment_details(self, apple_id: EmailStr, apple_id_password: SecretStr):
#     apple_pay_model = ApplePay(apple_id=apple_id, password=apple_id_password)
#     self.__payment_model.set_payment_method(ApplePayStrategy(apple_pay_model))
#     return self.__payment_model.get_payment_details()
