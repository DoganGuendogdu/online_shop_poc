from abc import ABC
from abc import abstractmethod
from datetime import datetime


class PaymentMethodStrategy(ABC):

    @abstractmethod
    def print_payment_params(self):
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


class PayPalStrategy(PaymentMethodStrategy):
    def __init__(self, user_name: str, password: str):
        self.__user_name = user_name
        self.__password = password

    def print_payment_params(self):
        print("Paypal")
        print(f"User name: '{self.__user_name}'")
        print(f"Password: '{self.__password}'")


class CreditCardStrategy(PaymentMethodStrategy):
    def __init__(self, credit_card_number: int, expiration_date: datetime, cvc: int, first_name: str, last_name: str):

        self.__credit_card_number = credit_card_number
        self.__expiration_date = expiration_date
        self.__cvc = cvc
        self.__name = first_name + " " + last_name

        self.__check_cvc_length()

    # Polymorphism
    def print_payment_params(self):
        expiration_date_str = self.__expiration_date.strftime("%Y-%m-%d")

        print("Credit Card")
        print(f"Credit card number : '{self.__credit_card_number}'")
        print(f"Expiration date: '{expiration_date_str}'")
        print(f"CVC: {self.__cvc}")
        print(f"Name: {self.__name}")

    def __check_cvc_length(self):
        cvc_str = str(self.__cvc)
        if len(cvc_str) > 3:
            raise ValueError("CVC length can not be longer than 3 digits!")
        elif len(cvc_str) < 3:
            raise ValueError("CVC length can not be less than 3 digits!")


class PaysafeStrategy(PaymentMethodStrategy):
    def __init__(self, paysafe_code: int):
        self.__paysafe_code = paysafe_code

    # Polymorphism
    def print_payment_params(self):
        print("Paysafe")
        print(f"Paysafe code: '{self.__paysafe_code}'")


class ApplePayStrategy(PaymentMethodStrategy):
    def __init__(self, apple_id: str, password: str):
        self.__user_name = apple_id
        self.__password = password

    # Polymorphism
    def print_payment_params(self):
        print("ApplePay")
        print(f"Apple ID: '{self.__user_name}'")
        print(f"Password: '{self.__password}'")


class PaymentStrategy(PaymentMethodStrategy):
    def __init__(self):
        self.__payment_method = None
        self.__buyer_protection = None

    def set_payment_method(self, payment_method: PaymentMethodStrategy):
        self.__payment_method = payment_method

    def set_seller_protection_for_buyer(self, buyer_protection: BuyerProtectionStrategy):
        self.__buyer_protection = buyer_protection

    def print_payment_params(self):
        self.__payment_method.print_payment_params()

    def print_seller_protection_for_buyer(self):
        self.__buyer_protection.print_seller_protection_for_buyer()
