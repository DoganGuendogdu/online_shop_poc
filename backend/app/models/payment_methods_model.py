from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel, Field, SecretStr, EmailStr

from datetime import datetime

# TODO: Add correct data types and ensure input values to be valid

class PaymentMethodStrategy(ABC):
    @abstractmethod
    def get_payment_details(self):
        pass


class BuyerProtectionStrategy(ABC):
    @abstractmethod
    def print_seller_protection_for_buyer(self):
        pass


class PaypalBuyerProtectionStrategy(BuyerProtectionStrategy):
    def print_seller_protection_for_buyer(self):
        print("You have a PayPal buyer protection of 17 days.")


class CreditCardBuyerProtectionStrategy(BuyerProtectionStrategy):
    def print_seller_protection_for_buyer(self):
        print("You have a Credit card buyer protection of 20 days.")


class PaysafeBuyerProtectionStrategy(BuyerProtectionStrategy):
    def print_seller_protection_for_buyer(self):
        print("You have a Paysafe buyer protection of 100 days.")


class ApplePayBuyerProtectionStrategy(BuyerProtectionStrategy):
    def print_seller_protection_for_buyer(self):
        print("You have a Apple Pay protection of 200 days.")


class PayPalModel(BaseModel):
    email: EmailStr = Field(..., example="john.doe@gmail.com")
    # SecretStr ensures that no password is logged or exposed
    # Use syntactic salt 'get_secret_value()' to retrieve password
    password: SecretStr = Field(..., min_length=8, max_length=88)


class PayPalStrategy(PaymentMethodStrategy):
    def __init__(self, paypal_model: PayPalModel):
        self.__paypal_model = paypal_model

    def get_payment_details(self):
        return {
            "payment_method": "paypal",
            **self.__paypal_model.model_dump(exclude={"password"})
        }


class MasterCardModel(BaseModel):
    credit_card_number: str = Field(..., min_length=16, max_length=19, example="5555 5555 5555 4444")
    expiration_date: datetime = Field(..., example=datetime.now())
    # Numbers 100-999, so all 3-digit numbers
    cvc: int = Field(..., ge=100, le=999, example=123)
    first_name: str = Field(..., max_length=40, example="Peter")
    last_name: str = Field(..., max_length=40, example="Lustig")


class MasterCardStrategy(PaymentMethodStrategy):
    def __init__(self, credit_card_model: MasterCardModel):
        self.__credit_card_model = credit_card_model

    def get_payment_details(self):
        return {
            "payment_method": "credit_card",
            **self.__credit_card_model.model_dump(exclude={"cvc"})
        }


class PaySafeModel(BaseModel):
    paysafe_code: str = Field(..., max_length=18, example="21312312123")


class PaySafeStrategy(PaymentMethodStrategy):
    def __init__(self, paysafe_model: PaySafeModel):
        self.__paysafe_model = paysafe_model

    def get_payment_details(self):
        return {
            "payment_method": "paysafe",
            **self.__paysafe_model.model_dump()
        }


class ApplePayModel(BaseModel):
    apple_id: str = Field(..., example="dogan@outlook.de")
    password: str = Field(..., example="kndkjansdna82828")


class ApplePayStrategy(PaymentMethodStrategy):
    def __init__(self, apple_pay_model: ApplePayModel):
        self.__apple_pay_model = apple_pay_model

    def get_payment_details(self):
        return {
            "payment_method": "ApplePay",
            **self.__apple_pay_model.model_dump(exclude={"password"})
        }


class PaymentModel(PaymentMethodStrategy):
    def __init__(self):
        self.__payment_method = None
        self.__buyer_protection = None

    def set_payment_method(self, payment_method: PaymentMethodStrategy):
        self.__payment_method = payment_method

    def set_seller_protection_for_buyer(self, buyer_protection: BuyerProtectionStrategy):
        self.__buyer_protection = buyer_protection

    def get_payment_details(self):
        return self.__payment_method.get_payment_details()

    def print_seller_protection_for_buyer(self):
        self.__buyer_protection.print_seller_protection_for_buyer()
