from fastapi import APIRouter

from ..controller.process_payment_controller import ProcessPaymentController
from ..models.payment_methods_model import ApplePayModel
from ..models.payment_methods_model import CreditCardModel
from ..models.payment_methods_model import PayPalModel
from ..models.payment_methods_model import PaySafeModel

router = APIRouter()

process_payment_controller = ProcessPaymentController()


@router.post("/payment/paypal")
def get_PayPal_payment_details(paypal_payment: PayPalModel):
    return process_payment_controller.get_PayPal_payment_details(
        paypal_payment.email,
        paypal_payment.password)


@router.post("/payment/credit_card")
def get_credict_card_payment_details(credit_card_payment: CreditCardModel):
    return process_payment_controller.get_credit_card_payment_details(
        credit_card_payment.credit_card_number, credit_card_payment.expiration_date, credit_card_payment.cvc,
        credit_card_payment.first_name, credit_card_payment.last_name)


@router.post("/payment/paysafe")
def get_PaySafe_payment_details(paysafe_payment: PaySafeModel):
    return process_payment_controller.get_PaySafe_payment_details(paysafe_payment.paysafe_code)


@router.post("/payment/apple_pay")
def get_ApplePay_payment_details(apple_pay_payment: ApplePayModel):
    return process_payment_controller.get_ApplePay_payment_details(
        apple_pay_payment.apple_id, apple_pay_payment.password)
