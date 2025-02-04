from abc import ABC
from abc import abstractmethod
from datetime import datetime


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


class PayPalStrategy(PaymentMethodStrategy):
    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    def get_payment_details(self):
        return {
            "payment_method": "PayPal",
            "user_name": self.user_name,
            "password": self.password
        }


class CreditCardStrategy(PaymentMethodStrategy):
    def __init__(self, credit_card_number: int, expiration_date: datetime, cvc: int, first_name: str, last_name: str):

        self.__credit_card_number = credit_card_number
        self.__expiration_date = expiration_date
        self.__cvc = cvc
        self.__name = first_name + " " + last_name

        self.__check_cvc_length()

    # Polymorphism
    def get_payment_details(self):
        expiration_date_str = self.__expiration_date.strftime("%Y-%m-%d")

        return {
            "payment_method": "Credit Card",
            "credit_card_number": self.__credit_card_number,
            "expiration_date": expiration_date_str,
            "cvc": self.__cvc,
            "name": self.__name
        }

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
    def get_payment_details(self):
        return {
            "payment_method": "Paysafe",
            "paysafe_code": self.__paysafe_code
        }


class ApplePayStrategy(PaymentMethodStrategy):
    def __init__(self, apple_id: str, password: str):
        self.__user_name = apple_id
        self.__password = password

    # Polymorphism
    def get_payment_details(self):
        return {
            "payment_method": "ApplePay",
            "apple_id": self.__user_name,
            "password": self.__password
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
