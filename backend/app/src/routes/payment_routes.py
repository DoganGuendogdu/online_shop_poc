from fastapi import APIRouter
from fastapi import status

from ..controller.payment_controller import PaymentController
from ..entities.payments import ApplePay
from ..entities.payments import MasterCard
from ..entities.payments import PayPal
from ..entities.payments import PaySafe

router = APIRouter()

payment_controller = PaymentController()


@router.post("/payment/paypal")
def get_PayPal_payment_details(paypal_payment: PayPal):
    return payment_controller.get_PayPal_payment_details(paypal_payment.email, paypal_payment.password)


@router.post("/payment/master_card")
def get_credict_card_payment_details(credit_card_payment: MasterCard):
    return payment_controller.get_master_card_payment_details(
        credit_card_payment.credit_card_number, credit_card_payment.expiration_date, credit_card_payment.cvc,
        credit_card_payment.first_name, credit_card_payment.last_name)


# @router.post("/payment/paysafe")
# def get_PaySafe_payment_details(paysafe_data: dict[str, int]):
#     if len(str(paysafe_data.get("paysafe_code"))) > 16:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="The provided paysafe code contains more than 16 digits.")
#
#     return payment_controller.get_PaySafe_payment_details(**paysafe_data)


@router.post("/payment/paysafe")
def get_PaySafe_payment_details(paysafe_payment: PaySafe):
    return payment_controller.get_PaySafe_payment_details(paysafe_payment.paysafe_code)


@router.post("/payment/apple_pay")
def get_ApplePay_payment_details(apple_pay_payment: ApplePay):
    return payment_controller.get_ApplePay_payment_details(
        apple_pay_payment.apple_id, apple_pay_payment.password)
