from ..service.payment_service import PaymentService
from ..views.payment_view import PaymentView


class PaymentController:
    def __init__(self, payment_view: PaymentView, payment_service: PaymentService):
        self.__payment_view = payment_view
        self.__payment_service = payment_service

    def call_payment_api(self):
        payment_input_data = self.__payment_view.handle_payment()
        if payment_input_data:
            self.__payment_service.post_payment(payment_input_data)
