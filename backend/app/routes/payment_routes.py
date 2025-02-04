from datetime import datetime

from fastapi import APIRouter

from ..controller.process_payment_controller import ProcessPaymentController
from ..models.payment_methods_model import PayPalStrategy

router = APIRouter()

process_payment_controller = ProcessPaymentController()


@router.post("/payment/paypal")
def get_PayPal_payment_details(paypal_payment: PayPalStrategy):
    return process_payment_controller.get_PayPal_payment_details(paypal_payment.paypal_user_name,
                                                                 paypal_payment.paypal_password)


@router.post("/payment/credit_card}")
def get_credict_card_payment_details(credit_card_number: int, expiration_date: datetime, cvc_number: int,
                                     first_name: str, last_name: str):
    return process_payment_controller.get_credict_card_payment_details(credit_card_number, expiration_date, cvc_number,
                                                                       first_name, last_name)


@router.post("/payment/paysafe")
def get_PaySafe_payment_details(paysafe_code: int):
    return process_payment_controller.get_PaySafe_payment_details(paysafe_code)


@router.post("/payment/apple_pay")
def get_ApplePay_payment_details(apple_id: str, apple_id_password: str):
    return process_payment_controller.get_ApplePay_payment_details(apple_id, apple_id_password)
